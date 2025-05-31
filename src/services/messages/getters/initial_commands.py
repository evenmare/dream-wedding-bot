"""Module contains initial command getter."""

from entities.enums.initial_commands import InitialCommandEnum
from entities.schemas.callbacks import CommandSchema
from exceptions.repositories import ObjectNotFoundException
from exceptions.services import CallbackMessageNotFoundException
from repositories.database.callbacks import CallbackMessageRepository
from services.messages.getters.base import BaseMessageDataGetter
from typings.services import MessageFactoryDataTuple


class InitialCommandDataGetter(
    BaseMessageDataGetter[
        MessageFactoryDataTuple[CommandSchema[str | None]],
    ]
):
    """Initial command response data service."""

    async def __call__(
        self,
        *,
        initial_command: InitialCommandEnum,
    ) -> MessageFactoryDataTuple[CommandSchema[str | None]]:
        """Get initial command response base data.

        :param initial_command: Initial command.
        :return: MessageSchema, list of CommandSchema.
        """
        try:
            callback_message = await self._callback_message_repository.get_by_initial_command(initial_command=initial_command)
        except ObjectNotFoundException as exc:
            raise CallbackMessageNotFoundException from exc

        commands = [
            _
            async for _ in self._command_repository.filter_by_initial_command(initial_command=initial_command)
        ]

        return MessageFactoryDataTuple(
            message_ref=callback_message,
            commands=commands,
        )
