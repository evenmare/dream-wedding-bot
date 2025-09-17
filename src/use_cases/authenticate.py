"""Module contains Use Case for authentication."""

from entities.schemas.guests import GuestSchema
from entities.schemas.telegram import TelegramUserSchema
from exceptions.repositories import ObjectNotFoundException
from exceptions.use_cases import NotAuthenticatedException
from repositories.database.guests import GuestRepository
from repositories.database.telegram import TelegramUserRepository


class AuthenticationUseCase:
    """Use Case implements an authentication logic."""

    def __init__(
        self,
        guest_repository: GuestRepository,
        telegram_user_repository: TelegramUserRepository,
    ) -> None:
        """Class constructor.

        :param guest_repository: Guest repository.
        :param telegram_user_repository: Telegram user repository.
        """
        self.__guest_repository = guest_repository
        self.__telegram_user_repository = telegram_user_repository

    async def __call__(self, user_schema: TelegramUserSchema) -> GuestSchema:
        """Authenticate user.

        :param user_id: User chat id.
        :param user_schema: Telegram user schema.
        :raises NotAuthenticatedException: If guest is not found.
        :return: Guest schema.
        """
        try:
            guest_schema: GuestSchema = await self.__guest_repository.get_by_telegram_user_id(user_id=user_schema.user_id)
        except ObjectNotFoundException as exc:
            raise NotAuthenticatedException from exc

        await self.__telegram_user_repository.update_or_create_by_guest_id(
            guest_id=guest_schema.guest_id,
            telegram_user=user_schema,
        )
        return guest_schema
