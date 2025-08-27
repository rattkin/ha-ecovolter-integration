"""Sensor platform for ecovolter."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from .utils import camel_to_snake
from .const import DOMAIN
from .entity import IntegrationEcovolterEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EcovolterDataUpdateCoordinator
    from .data import IntegrationEcovolterConfigEntry

# Key is used to get the value from the API
ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="actualPower",
        name="Nabíjecí výkon",
        icon="mdi:flash",
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="kW",
    ),
    SensorEntityDescription(
        key="chargedEnergy",
        name="Nabitá energie",
        icon="mdi:battery-charging",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="kWh",
    ),
    SensorEntityDescription(
        key="chargingCost",
        name="Cena nabíjení",
        icon="mdi:currency-eur",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="chargingTime",
        name="Doba nabíjení",
        icon="mdi:timer",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="s",
    ),
    SensorEntityDescription(
        key="remainingBoostTime",
        name="Zbývající boost čas",
        icon="mdi:timer-sand",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="s",
    ),
    SensorEntityDescription(
        key="currentL1",
        name="Proud L1",
        icon="mdi:alpha-l-circle",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="currentL2",
        name="Proud L2",
        icon="mdi:alpha-l-circle",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="currentL3",
        name="Proud L3",
        icon="mdi:alpha-l-circle",
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="voltageL1",
        name="Napětí L1",
        icon="mdi:alpha-v-circle",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="voltageL2",
        name="Napětí L2",
        icon="mdi:alpha-v-circle",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="voltageL3",
        name="Napětí L3",
        icon="mdi:alpha-v-circle",
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="V",
    ),
    SensorEntityDescription(
        key="temperatureCurrentLimit",
        name="Teplotní limit proudu",
        icon="mdi:thermometer-alert",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="adapterMaxCurrent",
        name="Max proud adaptéru",
        icon="mdi:flash-alert",
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="A",
    ),
    SensorEntityDescription(
        key="internalTemperature",
        name="Vnitřní teplota",
        icon="mdi:thermometer",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="totalChargedEnergy",
        name="Celková nabitá energie",
        icon="mdi:battery-charging",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement="kWh",
    ),
    SensorEntityDescription(
        key="totalChargingCount",
        name="Počet nabíjení",
        icon="mdi:counter",
        state_class=SensorStateClass.TOTAL,
    ),
    SensorEntityDescription(
        key="totalChargingTime",
        name="Celkový čas nabíjení",
        icon="mdi:timer",
        state_class=SensorStateClass.TOTAL,
        native_unit_of_measurement="s",
    ),
    SensorEntityDescription(
        key="maxInternalTemp",
        name="Max vnitřní teplota",
        icon="mdi:thermometer-chevron-up",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="°C",
    ),
    SensorEntityDescription(
        key="minInternalTemp",
        name="Min vnitřní teplota",
        icon="mdi:thermometer-chevron-down",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement="°C",
    ),
    # Add more for adapter/relay temps if needed
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationEcovolterConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        IntegrationEcovolterSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class IntegrationEcovolterSensor(IntegrationEcovolterEntity, SensorEntity):
    """ecovolter sensor class."""

    def __init__(
        self,
        coordinator: EcovolterDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{camel_to_snake(entity_description.key)}"
        )
        self._attr_name = entity_description.name

    @property
    def suggested_object_id(self) -> str:
        """This is used to generate the entity_id."""
        return f"{DOMAIN}_{camel_to_snake(self.entity_description.key)}"

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        value = self.coordinator.data.get("status", {}).get(self.entity_description.key)
        
        # Handle different data types and conversions
        if value is None:
            return None
            
        # Convert to float for numeric sensors
        try:
            return float(value)
        except (ValueError, TypeError):
            return value
