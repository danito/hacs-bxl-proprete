"""DataUpdateCoordinator for Bruxelles Propreté waste collection."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BxlPropreteAPI, BxlPropreteError
from .const import CONF_COMMUNE, CONF_NUMBER, CONF_STREET, CONF_ZIP, DEFAULT_SCAN_INTERVAL_HOURS

_LOGGER = logging.getLogger(__name__)


class BxlPropreteCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Bruxelles Propreté",
            update_interval=timedelta(hours=DEFAULT_SCAN_INTERVAL_HOURS),
        )
        self.config = config
        self.api = BxlPropreteAPI(async_get_clientsession(hass))

    async def _async_update_data(self):
        try:
            return await self.api.get_calendar(
                self.config[CONF_STREET],
                self.config[CONF_NUMBER],
                self.config[CONF_ZIP],
                self.config[CONF_COMMUNE],
            )
        except BxlPropreteError as err:
            raise UpdateFailed(str(err)) from err
