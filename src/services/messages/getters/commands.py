"""Module contains class for command response data getter."""

from entities.schemas.commands import CommandSchema
from entities.schemas.guests import GuestSchema
from exceptions.repositories import ObjectNotFoundException
from exceptions.services import CallbackMessageNotFoundException
from services.messages.getters.base import BaseMessageDataGetter
from typings.services import MessageFactoryDataTuple


class CommandMessageDataGetter(
    BaseMessageDataGetter[
        MessageFactoryDataTuple[CommandSchema[str]],
    ]
):
    """Command response data service."""

    async def __call__(
        self,
        *,
        guest: GuestSchema,
        command: CommandSchema[str],
    ) -> MessageFactoryDataTuple[CommandSchema[str]]:
        """Get command response base data.

        :param guest_form: Guest form schema.
        :param command: Command schema.
        :return: Message factory data.
        """
        try:
            callback_message = await self._callback_message_repository.get_by_command_id(command_id=command.command_id)
        except ObjectNotFoundException as exc:
            raise CallbackMessageNotFoundException from exc

        available_commands = [
            _ async for _ in self._command_repository.filter_available(guest_id=guest.guest_id)
        ]

        return MessageFactoryDataTuple(
            message_ref=callback_message,
            commands=available_commands,
        )
