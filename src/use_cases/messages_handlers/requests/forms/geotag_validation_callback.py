"""Module contains handler for INVITATION_GEOTAG_VALIDATION form stage."""

from entities.enums.forms import GuestFormStageEnum
from entities.schemas.commands import CommandSchema
from entities.schemas.forms import GuestFormSchema
from entities.schemas.invitations import InvitationRequestSchema
from repositories.database.forms import GuestFormRepository
from repositories.database.invitations import InvitationRequestRepository
from typings.use_cases import GuestInfoDataTuple
from use_cases.messages_handlers.requests.forms.base import BaseHandleFormCallbackUseCase


class HandleGeotagValidationCallbackUseCase(BaseHandleFormCallbackUseCase):
    """Class contains INVITATION_GEOTAG_VALIDATION callback handler logic."""

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

    async def __call__(self, *, guest_form: GuestFormSchema, callback_command: CommandSchema[str]) -> GuestInfoDataTuple:
        """Handle invitation callback.

        :param guest_form: Guest form.
        :param callback_command: Command.
        :return: Updated guest form.
        """
        new_form_stage = (
            GuestFormStageEnum.INVITATION_ADDRESS_TEXT_INPUT
            if callback_command.is_negative_feedback
            else GuestFormStageEnum.INVITATION_INFO_SPECIFICATION
        )

        guest_form.stage = new_form_stage
        await self.__guest_form_repository.partial_update(guest_form=guest_form)

        invitation_request = None
        if callback_command.is_negative_feedback:
            invitation_request = InvitationRequestSchema(guest_id=guest_form.guest_id, address=None)
            await self.__invitation_request_repository.partial_update(invitation_request=invitation_request)

        return GuestInfoDataTuple(
            guest_form=guest_form,
            invitation_request=invitation_request,
        )
