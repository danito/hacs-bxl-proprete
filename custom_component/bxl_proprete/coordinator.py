from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import BxlPropreteAPI
from .const import CONF_STREET, CONF_NUMBER, CONF_ZIP, CONF_COMMUNE

_LOGGER = logging.getLogger(__name__)

class BxlPropreteCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        super().__init__(hass, _LOGGER, name="Bxl Proprete", update_interval=timedelta(hours=12))
        self.config = config
        self.api = BxlPropreteAPI(async_get_clientsession(hass))

    async def _async_update_data(self):
        try:
            return await self.api.get_calendar(
                self.config[CONF_STREET],
                self.config[CONF_NUMBER],
                self.config[CONF_ZIP],
                self.config[CONF_COMMUNE]
            )
        except Exception as err:
            raise UpdateFailed(f"API communication error: {err}")