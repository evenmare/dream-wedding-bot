"""Module contains handler for INVITATION_NEEDINESS form stage."""

from entities.enums.forms import GuestFormStageEnum
from entities.schemas.callbacks import CommandSchema
from entities.schemas.forms import GuestFormSchema
from entities.schemas.invitations import InvitationRequestSchema
from repositories.database.forms import GuestFormRepository
from repositories.database.invitations import InvitationRequestRepository
from typings.use_cases import GuestInfoDataTuple
from use_cases.messages_handlers.requests.forms.base import BaseHandleFormCallbackUseCase


class HandleInvitationNeedinessCallbackUseCase(BaseHandleFormCallbackUseCase):
    """Class contains INVITATION_NEEDINESS callback handler logic."""

    def __init__(
        self,
        guest_form_repository: GuestFormRepository,
        invitation_request_repository: InvitationRequestRepository,
    ) -> None:
        """Class constructor.

        :param guest_form_repository: Guest form repository.
        :param invitation_request_repository: Invitation request repository.
        """
        self.__guest_form_repository = guest_form_repository
        self.__invitation_request_repository = invitation_request_repository

    async def __call__(self, *, guest_form: GuestFormSchema, callback_command: CommandSchema) -> GuestInfoDataTuple:
        """Handle callback command input.

        :param guest_form: Guest form.
        :param callback_command: Callback command.
        :return: Updated guest form.
        """
        new_form_stage = (
            GuestFormStageEnum.FILLING_ADDITIONAL_INFO
            if callback_command.is_negative_feedback
            else GuestFormStageEnum.INVITATION_ADDRESS_INPUT
        )

        guest_form.stage = new_form_stage
        await self.__guest_form_repository.partial_update(guest_form=guest_form)

        invitation_request = None
        if not callback_command.is_negative_feedback:
            invitation_request = InvitationRequestSchema(guest_id=guest_form.guest_id)
            await self.__invitation_request_repository.create(invitation_request=invitation_request)

        return GuestInfoDataTuple(
            guest_form=guest_form,
            invitation_request=invitation_request,
        )
