"""Constants for the solax integration."""

from functools import cache
from importlib.metadata import entry_points

from solax.inverter import Inverter

DOMAIN = "zago_solax"

MANUFACTURER = "(Zago) SolaX Power"

CONF_INVERTER_TYPE = "inverter_type"
INVERTER_TYPE_AUTO = "auto"


@cache
def get_inverter_entry_points() -> dict[str, type[Inverter]]:
    """Return the inverter classes registered by the solax library."""
    inverter_types: dict[str, type[Inverter]] = {}

    for entry_point in entry_points(group="solax.inverter"):
        inverter_type = entry_point.load()
        if isinstance(inverter_type, type) and issubclass(inverter_type, Inverter):
            inverter_types[entry_point.name] = inverter_type

    return inverter_types


def get_inverter_types() -> list[str]:
    """Return the names of inverter types registered by the solax library."""
    return sorted(get_inverter_entry_points())
