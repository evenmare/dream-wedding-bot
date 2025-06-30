"""Module contains repositories for Telegram models."""

from collections.abc import AsyncGenerator
from entities.database.telegram import TelegramUser
from entities.schemas.telegram import TelegramUserSchema
from repositories.database.base import BaseDatabaseRepository

__all__ = ('TelegramUserRepository',)


class TelegramUserRepository(BaseDatabaseRepository[TelegramUser, TelegramUserSchema]):
    """Class implements repository for Telegram users."""

    schema = TelegramUserSchema
    _model = TelegramUser

    async def filter_by_guests_ids(
        self,
        guests_ids: frozenset[int],
    ) -> AsyncGenerator[tuple[int, TelegramUserSchema], None]:
        """Filter all telegram users by guests ids.

        :param guests_ids: Guests identities.
        """
        query = self._model.filter(guest_id__in=guests_ids)

        users_iterator = aiter(query)

        async for user_orm in users_iterator:
            yield (user_orm.guest_id, self._serialize_model(user_orm))


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
        user_orm, _ = await self._model.update_or_create(
            guest_id=guest_id,
            defaults=telegram_user.model_dump(),
        )
        return self._serialize_model(user_orm)
