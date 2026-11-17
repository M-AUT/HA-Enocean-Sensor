from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.core import callback
from homeassistant.helpers.event import async_call_later

from .entity import EnOceanEntity

VIBRATION_HOLD = 15  # Sekunden


async def async_setup_entry(hass, entry, async_add_entities):
    hub = entry.runtime_data
    async_add_entities([EnOceanContact(entry, hub), EnOceanVibration(entry, hub)])


class EnOceanContact(EnOceanEntity, BinarySensorEntity):
    """on = offen (Magnet entfernt), off = geschlossen."""

    _attr_device_class = BinarySensorDeviceClass.DOOR

    def __init__(self, entry, hub):
        super().__init__(entry, hub, "contact_open", "Kontakt")
        self._attr_is_on = None

    def _apply(self, data) -> None:
        if "contact_open" in data:
            self._attr_is_on = data["contact_open"]


class EnOceanVibration(EnOceanEntity, BinarySensorEntity):
    """on fuer 15 s nach einem Beschleunigungs-Wake (Tuer bewegt)."""

    _attr_device_class = BinarySensorDeviceClass.MOVING

    def __init__(self, entry, hub):
        super().__init__(entry, hub, "vibration", "Bewegung")
        self._attr_is_on = False
        self._unsub = None

    def _apply(self, data) -> None:
        if data.get("acc_status") == 2:
            self._attr_is_on = True
            if self._unsub:
                self._unsub()
            self._unsub = async_call_later(self.hass, VIBRATION_HOLD, self._off)

    @callback
    def _off(self, _now) -> None:
        self._unsub = None
        self._attr_is_on = False
        self.async_write_ha_state()
