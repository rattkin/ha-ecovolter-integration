"""Number platform for ecovolter."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.number import NumberEntity, NumberEntityDescription

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
    NumberEntityDescription(
        key="targetCurrent",
        name="Požadovaný výkon",
        icon="mdi:current-ac",
        native_min_value=6,
        native_max_value=16,
        native_step=1,
        native_unit_of_measurement="A",
    ),
    NumberEntityDescription(
        key="boostTime",
        name="Boost čas",
        icon="mdi:timer-sand",
        native_min_value=0,
        native_max_value=43200,
        native_step=60,
        native_unit_of_measurement="s",
    ),
    NumberEntityDescription(
        key="boostCurrent",
        name="Boost proud",
        icon="mdi:flash",
        native_min_value=6,
        native_max_value=32,
        native_step=1,
        native_unit_of_measurement="A",
    ),
    NumberEntityDescription(
        key="kwhPrice",
        name="Cena za kWh",
        icon="mdi:currency-eur",
        native_min_value=0,
        native_max_value=100,
        native_step=0.01,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationEcovolterConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    async_add_entities(
        IntegrationEcovolterNumber(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class IntegrationEcovolterNumber(IntegrationEcovolterEntity, NumberEntity):
    """ecovolter number class."""

    def __init__(
        self,
        coordinator: EcovolterDataUpdateCoordinator,
        entity_description: NumberEntityDescription,
    ) -> None:
        """Initialize the number class."""
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
    def native_value(self) -> float:
        """Return the current value."""
        return self.coordinator.data.get("settings", {}).get(
            self.entity_description.key, 6
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set a new value."""
        await self.coordinator.config_entry.runtime_data.client.async_set_settings(
            {self.entity_description.key: int(value)}
        )
        await self.coordinator.async_request_refresh()
