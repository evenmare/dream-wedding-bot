"""Module contains repository for guests access."""

from entities.database.guests import Guest
from entities.enums.guests import GuestStatusEnum
from entities.schemas.guests import GuestSchema
from repositories.database.base import BaseDatabaseRepository

__all__ = ('GuestsRepository',)


class GuestsRepository(BaseDatabaseRepository[Guest, GuestSchema]):
    """Class implements repository for guests entity operations."""

    schema = GuestSchema
    __model = Guest

    async def get_by_chat_id(self, chat_id: int) -> GuestSchema:
        """Get guest by telegram chat id.

        :param chat_id: Telegram user chat id.
        :return: Guest schema object.
        """
        guest_orm = await self.__model.get(telegram_user__id=chat_id)
        return self._serialize_model(guest_orm)

    async def filter_by_phone_number(self, phone_number: str) -> GuestSchema | None:
        """Get guest by telegram phone number.

        :param phone_number: Guest phone number.
        :return: Guest schema object if exists, None otherwise.
        """
        guest_orm = await self.__model.get_or_none(phone_number=phone_number)

        if not guest_orm:
            return None

        return self._serialize_model(guest_orm)

    async def update_status(
        self,
        guest_id: int,
        status: GuestStatusEnum,
    ) -> None:
        """Update guest state.

        :param guest_id: Guest id.
        :param status: New Guest status.
        :return: Guest schema object.
        """
        await self.__model.filter(id=guest_id).update(status=status)
