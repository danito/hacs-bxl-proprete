"""Sensor platform for Bruxelles Propreté waste collection."""
from __future__ import annotations

import datetime as dt
import logging

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DAY_NAME_TO_WEEKDAY, DESC_RAMASSAGE_DAY_OFFSET, DOMAIN
from .coordinator import BxlPropreteCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: BxlPropreteCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            BxlPropreteNextGreenBagSensor(coordinator, entry),
            BxlPropreteNextWeeklyCollectionSensor(coordinator, entry),
        ]
    )


class BxlPropreteNextGreenBagSensor(CoordinatorEntity[BxlPropreteCoordinator], SensorEntity):
    """Next green bag (garden waste) collection date, from the SacsVerts list."""

    _attr_device_class = SensorDeviceClass.DATE
    _attr_icon = "mdi:leaf"
    _attr_has_entity_name = True
    _attr_name = "Next green bag collection"

    def __init__(self, coordinator: BxlPropreteCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_next_green_bag"

    @property
    def native_value(self) -> dt.date | None:
        upcoming = self._upcoming_dates()
        return upcoming[0] if upcoming else None

    @property
    def extra_state_attributes(self) -> dict:
        upcoming = self._upcoming_dates(10)
        attrs: dict = {"upcoming_dates": [d.isoformat() for d in upcoming]}
        if upcoming:
            attrs["days_until"] = (upcoming[0] - dt.date.today()).days
            attrs["human_readable"] = self._human_readable(upcoming[0])
        # img_ramassage is provided by ARP-GAN but is known to sometimes not
        # match the actual schedule for an address — use for display only.
        img = (self.coordinator.data or {}).get("img_ramassage", "").strip()
        if img:
            attrs["calendar_image_url"] = img
        return attrs

    def _upcoming_dates(self, limit: int = 10) -> list[dt.date]:
        today = dt.date.today()
        raw = (self.coordinator.data or {}).get("SacsVerts", [])
        dates = sorted(dt.date.fromisoformat(d) for d in raw if d)
        return [d for d in dates if d >= today][:limit]

    @staticmethod
    def _human_readable(target: dt.date) -> str:
        days = (target - dt.date.today()).days
        if days == 0:
            return "today"
        if days == 1:
            return "tomorrow"
        return f"in {days} days"


class BxlPropreteNextWeeklyCollectionSensor(CoordinatorEntity[BxlPropreteCoordinator], SensorEntity):
    """Next recurring bag collection day, computed from desc_ramassage.

    Note: ARP-GAN's desc_ramassage day labels are consistently one day later
    than the actual pickup day (confirmed against the household's physical
    collection days and against ARP-GAN's own calendar graphic, which is
    correct). DESC_RAMASSAGE_DAY_OFFSET in const.py corrects for this.
    SacsVerts (green bag dates) is NOT affected.
    """

    _attr_device_class = SensorDeviceClass.DATE
    _attr_icon = "mdi:trash-can"
    _attr_has_entity_name = True
    _attr_name = "Next bag collection"

    def __init__(self, coordinator: BxlPropreteCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_next_weekly_collection"

    @property
    def native_value(self) -> dt.date | None:
        next_day, _ = self._next_collection()
        return next_day

    @property
    def extra_state_attributes(self) -> dict:
        next_day, desc = self._next_collection()
        schedule = {
            day: text
            for day, text in (self.coordinator.data or {}).get("desc_ramassage", {}).items()
            if day != "message" and text
        }
        attrs: dict = {"weekly_schedule": schedule, "description": desc}
        if next_day:
            attrs["days_until"] = (next_day - dt.date.today()).days
            attrs["human_readable"] = self._human_readable(next_day)
        # img_ramassage is provided by ARP-GAN but is known to sometimes not
        # match the actual schedule for an address — use for display only.
        img = (self.coordinator.data or {}).get("img_ramassage", "").strip()
        if img:
            attrs["calendar_image_url"] = img
        return attrs

    def _next_collection(self) -> tuple[dt.date | None, str | None]:
        desc_ramassage = (self.coordinator.data or {}).get("desc_ramassage", {})
        today = dt.date.today()
        active_days = {
            (DAY_NAME_TO_WEEKDAY[day] + DESC_RAMASSAGE_DAY_OFFSET) % 7: text
            for day, text in desc_ramassage.items()
            if day in DAY_NAME_TO_WEEKDAY and text
        }
        if not active_days:
            return None, None
        for offset in range(8):
            candidate = today + dt.timedelta(days=offset)
            if candidate.weekday() in active_days:
                return candidate, active_days[candidate.weekday()]
        return None, None

    @staticmethod
    def _human_readable(target: dt.date) -> str:
        days = (target - dt.date.today()).days
        if days == 0:
            return "today"
        if days == 1:
            return "tomorrow"
        return f"in {days} days"
