"""Module contains geocoders infrastracture."""

from typing import AsyncGenerator
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim

from configs.infrastractures import GeocoderConfig


async def get_geocoder_client(config: GeocoderConfig) -> AsyncGenerator[Nominatim, None]:
    """Get geocoder client.

    :param config: Config for geocoder session.
    :yield: Geocoder client.
    """
    async with Nominatim(
        user_agent=config.USER_AGENT,
        adapter_factory=AioHTTPAdapter,
    ) as geocoder:
        yield geocoder
