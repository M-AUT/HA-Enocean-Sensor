"""EnOcean STM 550B / EMSWB BLE sensors."""
from __future__ import annotations

import logging

from homeassistant.components import bluetooth
from homeassistant.components.bluetooth import BluetoothCallbackMatcher
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import CONF_KEY, DOMAIN, SIGNAL
from .decoder import MANUFACTURER_ID, build_adv, parse, verify

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor", "binary_sensor"]


class Hub:
    def __init__(self, hass: HomeAssistant, address: str, key: bytes) -> None:
        self.hass = hass
        self.address = address
        self.key = key
        self.data: dict = {}
        self.last_seq = -1

    @callback
    def handle(self, service_info, change) -> None:
        payload = service_info.manufacturer_data.get(MANUFACTURER_ID)
        if not payload or len(payload) < 9:
            return
        adv = build_adv(bytes(payload))
        if not verify(self.key, self.address, adv):
            _LOGGER.debug("%s: Signatur ungueltig", self.address)
            return
        data = parse(adv)
        if data["seq"] <= self.last_seq:
            return
        self.last_seq = data["seq"]
        self.data.update(data)
        async_dispatcher_send(self.hass, SIGNAL.format(self.address), data)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    address = entry.data["address"].upper()
    hub = Hub(hass, address, bytes.fromhex(entry.data[CONF_KEY]))
    entry.runtime_data = hub
    entry.async_on_unload(
        bluetooth.async_register_callback(
            hass,
            hub.handle,
            BluetoothCallbackMatcher(address=address, connectable=False),
            bluetooth.BluetoothScanningMode.PASSIVE,
        )
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
