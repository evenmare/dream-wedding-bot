"""Module contains handler for AWAITING_ANSWER form stage."""

from entities.enums.forms import GuestFormStageEnum
from entities.schemas.commands import CommandSchema
from entities.schemas.forms import GuestFormSchema
from repositories.database.forms import GuestFormRepository
from typings.use_cases import GuestInfoDataTuple
from use_cases.messages_handlers.requests.forms.base import BaseHandleFormCallbackUseCase


class HandleAwaitingAnswerCallbackUseCase(BaseHandleFormCallbackUseCase):
    """Class contains AWAITING_ANSWER callback handler logic."""

    def __init__(self, guest_form_repository: GuestFormRepository) -> None:
        """Class constructor.

        :param guest_form_repository: Guest form repository.
        """
        self.__guest_form_repository = guest_form_repository

    async def __call__(self, *, guest_form: GuestFormSchema, callback_command: CommandSchema) -> GuestInfoDataTuple:
        """Handle callback command input.

        :param guest_form: Guest form.
        :param callback_command: Callback command.
        :return: Updated guest form.
        """
        new_form_stage = (
            GuestFormStageEnum.DECLINED
            if callback_command.is_negative_feedback
            else GuestFormStageEnum.INVITATION_NEEDINESS_ASKED
        )

        guest_form.stage = new_form_stage
        await self.__guest_form_repository.partial_update(guest_form=guest_form)

        return GuestInfoDataTuple(
            guest_form=guest_form,
            invitation_request=None,
        )
