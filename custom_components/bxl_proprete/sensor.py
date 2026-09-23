from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from datetime import date
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        BxlPropreteNextGreenBagSensor(coordinator),
        BxlPropreteScheduleSensor(coordinator)
    ])

class BxlPropreteNextGreenBagSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Next Green Bag Collection"
        self._attr_unique_id = f"{coordinator.config['street']}_{coordinator.config['number']}_green_bag"
        self._attr_icon = "mdi:leaf"

    @property
    def state(self):
        dates = self.coordinator.data.get("SacsVerts", [])
        today = date.today()
        future_dates = sorted([date.fromisoformat(d) for d in dates if date.fromisoformat(d) >= today])
        return future_dates[0].isoformat() if future_dates else None

class BxlPropreteScheduleSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Waste Collection Schedule"
        self._attr_unique_id = f"{coordinator.config['street']}_{coordinator.config['number']}_schedule"
        self._attr_icon = "mdi:trash-can"

    @property
    def state(self):
        return "OK"

    @property
    def extra_state_attributes(self):
        schedule = {}
        for day, desc in self.coordinator.data.get("desc_ramassage", {}).items():
            if day != "message" and desc:
                schedule[day.capitalize()] = desc
        return schedule