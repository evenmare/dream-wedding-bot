"""Module contains Use Case for callback query processing."""

from configs.use_cases import IdentifyCallbackQueryUseCaseConfig
from entities.schemas.callbacks import CommandSchema
from entities.schemas.guests import GuestSchema
from exceptions.repositories import ObjectNotFoundException
from exceptions.use_cases import CommandNotFoundException
from repositories.database.callbacks import CommandRepository


class IdentifyCallbackQueryUseCase:
    """Use case implements logic for handling callback."""

    def __init__(
        self,
        command_repository: CommandRepository,
        config: IdentifyCallbackQueryUseCaseConfig,
    ) -> None:
        """Class constructor.

        :param command_repository: Command repository.
        """
        self.__command_repository = command_repository
        self.config = config

    async def __call__(
        self,
        guest: GuestSchema,
        code: str | None = None,
        *,
        strict: bool = True,
    ) -> CommandSchema[str]:
        """Handle callback.

        :param code: Command code.
        :return: Command schema.
        """
        if code:
            try:
                return await self.__command_repository.get_available_by_code(
                    guest_id=guest.guest_id,
                    code=code,
                )
            except ObjectNotFoundException as exc:
                if strict:
                    raise CommandNotFoundException from exc

        try:
            return await self.__command_repository.get_available_by_code(
                guest_id=guest.guest_id,
                code=self.config.DEFAULT_COMMAND_CODE,
            )
        except ObjectNotFoundException as exc:
            raise CommandNotFoundException from exc
