"""Module contains handler for FILLING_ADDITIONAL_INFO form stage."""

from entities.enums.forms import GuestFormStageEnum
from entities.schemas.forms import GuestFormSchema
from repositories.database.forms import GuestFormRepository
from typings.use_cases import GuestInfoDataTuple
from use_cases.messages_handlers.requests.forms.base import BaseHandleFormCallbackUseCase


class HandleAdditionalInfoCallbackUseCase(BaseHandleFormCallbackUseCase):
    """Class contains FILLING_ADDITIONAL_INFO callback handler logic."""

    def __init__(
        self,
        guest_form_repository: GuestFormRepository,
    ) -> None:
        """Class constructor.

        :param guest_form_repository: Guest form repository.
        """
        self.__guest_form_repository = guest_form_repository

    async def __call__(self, *, guest_form: GuestFormSchema, additional_info: str) -> GuestInfoDataTuple:
        """Handle invitation callback.

        :param guest_form: Guest form.
        :param callback_command: Command.
        :return: Updated guest form.
        """
        new_form_stage = GuestFormStageEnum.COMPLETED

        guest_form.stage = new_form_stage
        guest_form.additional_info = additional_info
        await self.__guest_form_repository.partial_update(guest_form=guest_form)

        return GuestInfoDataTuple(
            guest_form=guest_form,
            invitation_request=None,
        )
