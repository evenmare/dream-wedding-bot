"""Module contains service of address getter from coordinates."""

from configs.services import GetAddressByLocationServiceConfig
from typings.services import CoordinatesTuple

from geopy.geocoders import Nominatim
from geopy.point import Point
from geopy.location import Location


class GetAddressByLocationService:
    """Service address defenition from coordinates tuple."""

    def __init__(
        self,
        geocoder: Nominatim,
        config: GetAddressByLocationServiceConfig,
    ):
        """Class constructor.

        :param geocoder: Geocoder session.
        """
        self.__geocoder = geocoder
        self.__config = config

    async def __call__(self, coordinates: CoordinatesTuple) -> str:
        """Get address from coordinates.

        :param coordinates: Coordinates tuple.
        :return: Address representation.
        """
        point = Point(*coordinates)
        location: Location = await self.__geocoder.reverse(
            point,
            language=self.__config.LANGUAGE_CODE,
        )
        return location.address
