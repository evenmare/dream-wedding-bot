"""Module contains repositories for Telegram models."""

from entities.database.telegram import TelegramUser
from entities.schemas.telegram import TelegramUserSchema
from repositories.database.base import BaseDatabaseRepository

__all__ = ('TelegramUsersRepository',)


class TelegramUsersRepository(BaseDatabaseRepository[TelegramUser, TelegramUserSchema]):
    """Class implements repository for Telegram users."""

    schema = TelegramUserSchema
    __model = TelegramUser

    async def update_or_create_by_guest_id(
        self,
        guest_id: int,
        telegram_user: TelegramUserSchema,
    ) -> TelegramUserSchema:
        """Updates or creates telegram user record.

        :param guest_id: Guest id.
        :param telegram_user: Telegram user schema.
        :return: Telegram user schema of created record.
        """
        user_orm, _ = await self.__model.update_or_create(
            guest_id=guest_id,
            defaults=telegram_user.model_dump(),
        )
        return self._serialize_model(user_orm)
