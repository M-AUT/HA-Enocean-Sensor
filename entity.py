from __future__ import annotations

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, SIGNAL


class EnOceanEntity(Entity):
    _attr_has_entity_name = True
    _attr_should_poll = False
    _key: str

    def __init__(self, entry, hub, key: str, name: str) -> None:
        self._hub = hub
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{hub.address}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, hub.address)},
            name=entry.data.get("name", hub.address),
            manufacturer="EnOcean",
            model="STM 550B / EMSWB",
        )

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, SIGNAL.format(self._hub.address), self._update
            )
        )
        self._apply(self._hub.data)

    def _apply(self, data) -> None:
        raise NotImplementedError

    @callback
    def _update(self, data) -> None:
        self._apply(data)
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        return self._key in self._hub.data or self._key == "vibration"
