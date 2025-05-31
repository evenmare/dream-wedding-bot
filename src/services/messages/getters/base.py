"""Module contains base abstract class for message factory."""

import abc

from entities.schemas.callbacks import CommandSchema
from entities.schemas.forms import GuestFormSchema
from repositories.database.callbacks import CallbackMessageRepository, CommandRepository
from typings.services import MessageFactoryDataTuple


class BaseMessageDataGetter[
    _MessageFactoryDataType = MessageFactoryDataTuple[CommandSchema[str | None]],
](abc.ABC):
    """Base abstract response data service."""

    def __init__(
        self,
        callback_message_repository: CallbackMessageRepository,
        command_repository: CommandRepository,
    ) -> None:
        """Class constructor.

        :param callback_message_repository: Callback messages repository.
        :param command_repository: Command repository.
        """
        self._callback_message_repository = callback_message_repository
        self._command_repository = command_repository

    @abc.abstractmethod
    async def __call__(
        self,
        *_,
        **__,
    ) -> _MessageFactoryDataType:
        """Get message data for factory.

        :return: Message factory data tuple.
        """
        raise NotImplementedError('__call__')
