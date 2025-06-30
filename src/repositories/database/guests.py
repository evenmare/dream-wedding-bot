"""Module contains repository for guests access."""

from typing import AsyncGenerator, Sequence

from tortoise.exceptions import DoesNotExist

from entities.database.guests import Guest
from entities.schemas.guests import GuestSchema
from exceptions.repositories import ObjectNotFoundException
from repositories.database.base import BaseDatabaseRepository

__all__ = ('GuestRepository',)


class GuestRepository(BaseDatabaseRepository[Guest, GuestSchema]):
    """Class implements repository for guests entity operations."""

    schema = GuestSchema
    _model = Guest

    async def get_by_guest_id(self, guest_id: int) -> GuestSchema:
        """Get guest record by id.

        :param guest_id: Guest identificator.
        :raises ObjectNotFoundException: If guest not found.
        :return: Guest schema.
        """
        try:
            guest_orm = await self._model.get(guest_id=guest_id)
        except DoesNotExist as exc:
            raise ObjectNotFoundException(
                details=f'Guest with guest_id={guest_id}',
            ) from exc

        return self._serialize_model(guest_orm)

    async def get_by_telegram_user_id(self, user_id: int) -> GuestSchema:
        """Get guest record by telegram user id.

        :param user_id: Telegram user identificator.
        :raises ObjectNotFoundException: If guest not found.
        :return: Guest schema.
        """
        try:
            guest_orm = await self._model.get(telegram_user__user_id=user_id)
        except DoesNotExist as exc:
            raise ObjectNotFoundException(
                details=f'Guest with telegram user_id={user_id}',
            ) from exc

        return self._serialize_model(guest_orm)

    async def filter_all(
        self,
        guests_ids: Sequence[int] | None = None,
    ) -> AsyncGenerator[GuestSchema, None]:
        """Filter guests by guests ids.

        :param guests_ids: Sequence of guests ids.
        :return: Async generator of guests.
        """
        query = self._model.all()

        if guests_ids:
            query = query.filter(guest_id__in=guests_ids)

        guests_iterator = aiter(query)

        async for guest_orm in guests_iterator:
            yield self._serialize_model(guest_orm)

    async def filter_by_phone_number(self, phone_number: str) -> GuestSchema | None:
        """Get guest record by phone number.

        :param phone_number: Guest phone number.
        :return: Guest schema object if exists, None otherwise.
        """
        guest_orm = await self._model.get_or_none(phone_number=phone_number)

        if not guest_orm:
            return None

        return self._serialize_model(guest_orm)
