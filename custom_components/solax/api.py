"""Helpers for creating a SolaX real-time API client."""

import asyncio
from collections.abc import Mapping
from typing import Any, cast

from solax import Inverter, RealTimeAPI, discover, real_time_api

from homeassistant.const import CONF_IP_ADDRESS, CONF_PASSWORD, CONF_PORT

from .const import (
    CONF_INVERTER_TYPE,
    INVERTER_TYPE_AUTO,
    get_inverter_entry_points,
)


async def async_create_api(data: Mapping[str, Any]) -> RealTimeAPI:
    """Create an API client using automatic or manual inverter discovery."""
    inverter_type = data.get(CONF_INVERTER_TYPE, INVERTER_TYPE_AUTO)

    if not inverter_type or inverter_type == INVERTER_TYPE_AUTO:
        return await real_time_api(
            data[CONF_IP_ADDRESS], data[CONF_PORT], data[CONF_PASSWORD]
        )

    inverter_class = get_inverter_entry_points().get(inverter_type)
    if inverter_class is None:
        raise ValueError(f"Unsupported inverter type: {inverter_type}")

    inverter = await discover(
        data[CONF_IP_ADDRESS],
        data[CONF_PORT],
        data[CONF_PASSWORD],
        inverters=[inverter_class],
        return_when=asyncio.FIRST_COMPLETED,
    )
    return RealTimeAPI(cast(Inverter, inverter))
