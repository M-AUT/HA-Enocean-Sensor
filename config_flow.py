from __future__ import annotations

import re

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow

from .const import CONF_KEY, DOMAIN


class EnOceanConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            addr = user_input["address"].strip().upper()
            key = user_input[CONF_KEY].strip().replace(" ", "")
            if not re.fullmatch(r"([0-9A-F]{2}:){5}[0-9A-F]{2}", addr):
                errors["address"] = "invalid_address"
            elif not re.fullmatch(r"[0-9A-Fa-f]{32}", key):
                errors[CONF_KEY] = "invalid_key"
            else:
                await self.async_set_unique_id(addr)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input["name"],
                    data={"address": addr, CONF_KEY: key, "name": user_input["name"]},
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name"): str,
                    vol.Required("address"): str,
                    vol.Required(CONF_KEY): str,
                }
            ),
            errors=errors,
        )
