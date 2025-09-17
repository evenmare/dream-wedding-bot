"""Module contains tests for service of address getter from coordinates."""

import pytest
from configs.services import GetAddressByLocationServiceConfig
from services.get_address_by_location import GetAddressByLocationService
from typings.services import CoordinatesTuple

from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim


@pytest.mark.webtest
async def test_get_address_by_location_service():
    """Validate service returns address on coordinates tuple."""
    coordinates = CoordinatesTuple(53.900725, 27.634231)
    config = GetAddressByLocationServiceConfig()

    async with Nominatim(
        user_agent='test_wedding_bot',
        adapter_factory=AioHTTPAdapter,
    ) as geocoder:
        service = GetAddressByLocationService(geocoder=geocoder, config=config)
        assert await service(coordinates=coordinates)
