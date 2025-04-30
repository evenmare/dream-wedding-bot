"""Module contains repository for guests access."""

from entities.database.guests import Guest
from entities.schemas.guests import GuestSchema
from repositories.database.base import BaseDatabaseRepository

__all__ = ('GuestRepository',)


class GuestRepository(BaseDatabaseRepository[Guest, GuestSchema]):
    """Class implements repository for guests entity operations."""

    schema = GuestSchema
    _model = Guest

    async def get_by_guest_id(self, guest_id: int) -> GuestSchema:
        """Get guest record by id.

        :param guest_id: Guest identity.
        :return: Guest schema.
        """
        guest_orm = await self._model.get(guest_id=guest_id)
        return self._serialize_model(guest_orm)

    async def filter_by_phone_number(self, phone_number: str) -> GuestSchema | None:
        """Get guest record by phone number.

        :param phone_number: Guest phone number.
        :return: Guest schema object if exists, None otherwise.
        """
        guest_orm = await self._model.get_or_none(phone_number=phone_number)

        if not guest_orm:
            return None

        return self._serialize_model(guest_orm)
