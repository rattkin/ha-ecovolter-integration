"""Custom types for ecovolter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import EcovolterApiClient
    from .coordinator import EcovolterDataUpdateCoordinator

@dataclass
class EcovolterData:
    """Data for the Ecovolter integration."""

    client: EcovolterApiClient
    coordinator: EcovolterDataUpdateCoordinator
    integration: Integration
