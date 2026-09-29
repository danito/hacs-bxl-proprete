"""Config flow for Bruxelles Propreté waste collection."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import BxlPropreteAPI, BxlPropreteError
from .const import CONF_COMMUNE, CONF_NUMBER, CONF_STREET, CONF_ZIP, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_STREET): str,
        vol.Required(CONF_NUMBER): str,
        vol.Required(CONF_ZIP): str,
        vol.Required(CONF_COMMUNE): str,
    }
)


class BxlPropreteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors: dict[str, str] = {}

        if user_input is not None:
            api = BxlPropreteAPI(async_get_clientsession(self.hass))
            try:
                data = await api.get_calendar(
                    user_input[CONF_STREET],
                    user_input[CONF_NUMBER],
                    user_input[CONF_ZIP],
                    user_input[CONF_COMMUNE],
                )
            except BxlPropreteError:
                errors["base"] = "invalid_address"
            except Exception:
                _LOGGER.exception("Unexpected error validating address")
                errors["base"] = "unknown"
            else:
                unique_id = (
                    f"{user_input[CONF_STREET]}_{user_input[CONF_NUMBER]}"
                    f"_{user_input[CONF_ZIP]}"
                ).lower()
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                # Use the canonical address string returned by the API as title
                title = data.get(
                    "rue", f"{user_input[CONF_STREET]} {user_input[CONF_NUMBER]}"
                )
                return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_SCHEMA, errors=errors
        )
