"""Module contains Use Case for forming response on command message."""

from entities.schemas.commands import CommandSchema
from entities.schemas.callbacks import MessageSchema
from entities.schemas.forms import GuestFormSchema
from entities.schemas.guests import GuestSchema
from entities.schemas.invitations import InvitationRequestSchema
from services.messages.factory import MessageFactoryService
from services.messages.getters.commands import CommandMessageDataGetter


class GetResponseMessageByCommandUseCase:
    """Use case implements logic for receiving response message by command."""

    def __init__(
        self,
        getter_service: CommandMessageDataGetter,
        factory_service: MessageFactoryService,
    ) -> None:
        """Class constructor.

        :param command_repository: Command repository.
        :param getter_service: Message factory data getter.
        :param factory_service: Factory service.
        """
        self.__getter_service: CommandMessageDataGetter = getter_service
        self.__factory_service: MessageFactoryService = factory_service

    async def __call__(
        self,
        command: CommandSchema,
        guest: GuestSchema,
        guest_form: GuestFormSchema | None = None,
        invitation_request: InvitationRequestSchema | None = None,
    ) -> MessageSchema:
        """Get response message for command.

        :param code: Code of command.
        :param guest: Guest schema.
        :param guest_form: Guest form schema.
        :return: Message schema.
        """
        message_factory_data = await self.__getter_service(
            guest=guest,
            command=command,
        )
        return await self.__factory_service(
            message_factory_data=message_factory_data,
            guest=guest,
            guest_form=guest_form,
            invitation_request=invitation_request,
        )
