"""Select platform for ecovolter."""

from __future__ import annotations
from typing import TYPE_CHECKING
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from .const import DOMAIN
from .entity import IntegrationEcovolterEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from .coordinator import EcovolterDataUpdateCoordinator
    from .data import IntegrationEcovolterConfigEntry

ENTITY_DESCRIPTIONS = (
    SelectEntityDescription(
        key="currency",
        name="Měna",
        icon="mdi:currency-sign",
        options=["EUR", "CZK", "USD"],
    ),
)

CURRENCY_MAP = {"EUR": 0, "CZK": 1, "USD": 2}
REVERSE_CURRENCY_MAP = {0: "EUR", 1: "CZK", 2: "USD"}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationEcovolterConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    async_add_entities(
        IntegrationEcovolterSelect(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )

class IntegrationEcovolterSelect(IntegrationEcovolterEntity, SelectEntity):
    """ecovolter select class."""

    def __init__(self, coordinator, entity_description):
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        self._attr_name = entity_description.name
        self._attr_options = entity_description.options

    @property
    def current_option(self):
        value = self.coordinator.data.get("settings", {}).get(self.entity_description.key)
        return REVERSE_CURRENCY_MAP.get(value, "EUR")

    async def async_select_option(self, option: str):
        value = CURRENCY_MAP.get(option, 0)
        await self.coordinator.config_entry.runtime_data.client.async_set_settings({self.entity_description.key: value})
        await self.coordinator.async_request_refresh()
