"""Config flow for solax integration."""

from __future__ import annotations

import logging
from typing import Any

from solax import real_time_api
from solax.discovery import DiscoveryError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_IP_ADDRESS, CONF_PASSWORD, CONF_PORT
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.selector import selector

from .const import DOMAIN, get_inverter_entry_points, get_inverter_types, SOLAX_CONF_INVERTER_TYPE

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 80
DEFAULT_PASSWORD = ""

def make_data_schema() -> vol.Schema:
    """Create the data schema."""
    return vol.Schema(
        {
            vol.Required(CONF_IP_ADDRESS): cv.string,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
            vol.Optional(CONF_PASSWORD, default=DEFAULT_PASSWORD): cv.string,
            vol.Optional(SOLAX_CONF_INVERTER_TYPE, default=""): selector({
                "select": {
                    "options": get_inverter_types()
                }
            }),
        }
    )

async def validate_api(data) -> str:
    """Validate the credentials."""

    api = await real_time_api(
        data[CONF_IP_ADDRESS], data[CONF_PORT], data[CONF_PASSWORD],
        inverters=[get_inverter_entry_points().get(data[SOLAX_CONF_INVERTER_TYPE])]
    )
    response = await api.get_data()
    return response.serial_number


class SolaxConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Solax."""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, Any] = {}
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=make_data_schema(), errors=errors
            )

        try:
            serial_number = await validate_api(user_input)
        except (ConnectionError, DiscoveryError):
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            await self.async_set_unique_id(serial_number)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=serial_number, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=make_data_schema(), errors=errors
        )
