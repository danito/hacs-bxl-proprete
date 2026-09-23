import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_STREET, CONF_NUMBER, CONF_ZIP, CONF_COMMUNE

class BxlPropreteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            title = f"{user_input[CONF_STREET]} {user_input[CONF_NUMBER]}"
            return self.async_create_entry(title=title, data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_STREET): str,
            vol.Required(CONF_NUMBER): str,
            vol.Required(CONF_ZIP): str,
            vol.Required(CONF_COMMUNE): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema
        )