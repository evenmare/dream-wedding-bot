"""Module contains Use Case for forming response on initial messages."""

from entities.enums.initial_commands import InitialCommandEnum
from entities.schemas.callbacks import MessageSchema
from services.messages.factory import MessageFactoryService
from services.messages.getters.initial_commands import InitialCommandDataGetter


class GetResponseMessageByInitialCommandUseCase:
    """Use case implements logic for receivin response message by initial command."""

    def __init__(
        self,
        getter_service: InitialCommandDataGetter,
        factory_service: MessageFactoryService,
    ) -> None:
        """Class constructor.

        :param getter_service: Message factory data getter.
        :param factory_service: Factory service.
        """
        self.__getter_service: InitialCommandDataGetter = getter_service
        self.__factory_service: MessageFactoryService = factory_service

    async def __call__(
        self,
        initial_command: InitialCommandEnum,
    ) -> MessageSchema:
        """Get response message for initial command.

        :param initial_command: Initial command.
        :return: Message schema.
        """
        message_factory_data = await self.__getter_service(initial_command=initial_command)
        return await self.__factory_service(message_factory_data=message_factory_data)
