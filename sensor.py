from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfTemperature

from .entity import EnOceanEntity

SENSORS = [
    ("temperature", "Temperatur", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS),
    ("humidity", "Luftfeuchte", SensorDeviceClass.HUMIDITY, PERCENTAGE),
    ("illuminance", "Helligkeit", SensorDeviceClass.ILLUMINANCE, "lx"),
    ("energy", "Energiespeicher", SensorDeviceClass.BATTERY, PERCENTAGE),
    ("acc_x", "Beschleunigung X", None, "g"),
    ("acc_y", "Beschleunigung Y", None, "g"),
    ("acc_z", "Beschleunigung Z", None, "g"),
]


async def async_setup_entry(hass, entry, async_add_entities):
    hub = entry.runtime_data
    async_add_entities(EnOceanSensor(entry, hub, *s) for s in SENSORS)


class EnOceanSensor(EnOceanEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, entry, hub, key, name, dev_class, unit):
        super().__init__(entry, hub, key, name)
        self._attr_device_class = dev_class
        self._attr_native_unit_of_measurement = unit
        self._attr_native_value = None

    def _apply(self, data) -> None:
        if self._key in data:
            self._attr_native_value = data[self._key]
