"""Module contains Use Case for forming response on form stage."""

from entities.schemas.callbacks import MessageSchema
from entities.schemas.forms import GuestFormSchema
from entities.schemas.guests import GuestSchema
from entities.schemas.invitations import InvitationRequestSchema
from services.messages.factory import MessageFactoryService
from services.messages.getters.forms import FormMessageDataGetter


class GetResponseMessageByFormStageUseCase:
    """Use case implements logic for receiving response message by form stage."""

    def __init__(
        self,
        getter_service: FormMessageDataGetter,
        factory_service: MessageFactoryService,
    ) -> None:
        """Class constructor.

        :param getter_service: Message factory data getter.
        :param factory_service: Factory service.
        """
        self.__getter_service: FormMessageDataGetter = getter_service
        self.__factory_service: MessageFactoryService = factory_service

    async def __call__(
        self,
        guest: GuestSchema,
        guest_form: GuestFormSchema,
        invitation_request: InvitationRequestSchema | None = None,
    ) -> MessageSchema:
        """Get response message for form stage.

        :param guest: Guest schema.
        :param guest_form: Guest form schema.
        :param invitation_request: Invitation request schema, defaults to None
        :return: Message schema.
        """
        message_factory_data = await self.__getter_service(guest_form=guest_form)
        return await self.__factory_service(
            message_factory_data=message_factory_data,
            guest=guest,
            guest_form=guest_form,
            invitation_request=invitation_request,
        )
