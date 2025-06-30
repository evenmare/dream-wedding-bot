"""Module contains base interface for form callbacks handling."""

from entities.schemas.forms import GuestFormSchema
from typings.use_cases import GuestInfoDataTuple


class BaseHandleFormCallbackUseCase:
    """Class implements base interface for form callbacks handling."""

    should_delete_reply_keyboard: bool = False

    async def __call__(self, *, guest_form: GuestFormSchema, **__) -> GuestInfoDataTuple:
        """Handle callback from guest in form filling.

        :param guest_form: Guest form schema.
        :return: Updated guest form.
        """
        raise NotImplementedError