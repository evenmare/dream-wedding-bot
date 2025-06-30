"""Module contains Use Case for registration."""

from entities.enums.forms import GuestFormStageEnum
from entities.schemas.forms import GuestFormSchema
from entities.schemas.guests import GuestSchema
from entities.schemas.telegram import TelegramUserSchema
from exceptions.use_cases import NotAuthenticatedException
from repositories.database.forms import GuestFormRepository
from repositories.database.guests import GuestRepository
from repositories.database.telegram import TelegramUserRepository


class RegistrationUseCase:
    """Use Case implements a registration logic."""

    def __init__(
        self,
        guest_repository: GuestRepository,
        guest_form_repository: GuestFormRepository,
        telegram_user_repository: TelegramUserRepository,
    ) -> None:
        """Class constructor.

        :param guest_repository: Guest repository.
        :param telegram_user_repository: Telegram user repository.
        """
        self.__guest_repository = guest_repository
        self.__guest_form_repository = guest_form_repository
        self.__telegram_user_repository = telegram_user_repository

    async def __call__(self, phone_number: str, user_schema: TelegramUserSchema) -> tuple[GuestSchema, GuestFormSchema]:
        """Register user.

        :param phone_number: Number of phone.
        :param user_schema: Telegram user info.
        :raises NotAuthenticatedException: If guest if not found.
        :return: Is registered?
        """
        phone_number = phone_number.removeprefix('+')
        guest_schema = await self.__guest_repository.filter_by_phone_number(phone_number=phone_number)

        if not guest_schema:
            raise NotAuthenticatedException()

        await self.__telegram_user_repository.update_or_create_by_guest_id(
            guest_id=guest_schema.guest_id,
            telegram_user=user_schema,
        )

        guest_form = GuestFormSchema(
            guest_id=guest_schema.guest_id,
            stage=GuestFormStageEnum.AWAITING_ANSWER,
        )
        await self.__guest_form_repository.create(guest_form=guest_form)

        return guest_schema, guest_form
