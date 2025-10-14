"""Constants for the solax integration."""

from importlib.metadata import entry_points

DOMAIN = "zago_solax"

MANUFACTURER = "(Zago) SolaX Power"

async def get_inverter_entry_points() -> dict[str, object]:
    """Return the dict of supported inverter entry points."""
    return await {
        ep.name: ep.load() for ep in entry_points(group="solax.inverter")
    }

async def get_inverter_types() -> list[str]:
    """Return the list of supported inverter types."""
    INVERTERS_ENTRY_POINTS = await get_inverter_entry_points()
    return list(INVERTERS_ENTRY_POINTS.keys())


SOLAX_CONF_INVERTER_TYPE = "inverter_type"
