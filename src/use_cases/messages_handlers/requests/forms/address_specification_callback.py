"""Module contains handler for INVITATION_ADDRESS_SPECIFICATION form stage."""

from entities.enums.forms import GuestFormStageEnum
from entities.schemas.forms import GuestFormSchema
from entities.schemas.invitations import InvitationRequestSchema
from repositories.database.forms import GuestFormRepository
from repositories.database.invitations import InvitationRequestRepository
from typings.use_cases import GuestInfoDataTuple
from use_cases.messages_handlers.requests.forms.base import BaseHandleFormCallbackUseCase


class HandleAddressSpecificationCallbackUseCase(BaseHandleFormCallbackUseCase):
    """Class contains INVITATION_ADDRESS_SPECIFICATION callback handler logic."""

    def __init__(
        self,
        guest_form_repository: GuestFormRepository,
        invitation_request_repository: InvitationRequestRepository,
    ) -> None:
        """Class constructor.

        :param guest_form_repository: Guest form repository.
        :param invitation_reqest_repository: Invitation request repository.
        """
        self.__guest_form_repository = guest_form_repository
        self.__invitation_request_repository = invitation_request_repository

    async def __call__(self, *, guest_form: GuestFormSchema, address_specification: str) -> GuestInfoDataTuple:
        """Handle invitation callback.

        :param guest_form: Guest form.
        :param callback_command: Command.
        :return: Updated guest form.
        """
        new_form_stage = GuestFormStageEnum.FILLING_ADDITIONAL_INFO

        guest_form.stage = new_form_stage
        await self.__guest_form_repository.partial_update(guest_form=guest_form)

        invitation_request = InvitationRequestSchema(
            guest_id=guest_form.guest_id,
            address_specification=address_specification,
        )
        await self.__invitation_request_repository.partial_update(invitation_request=invitation_request)

        invitation_request = await self.__invitation_request_repository.get_by_guest_id(guest_id=guest_form.guest_id)
        return GuestInfoDataTuple(
            guest_form=guest_form,
            invitation_request=invitation_request,
        )
