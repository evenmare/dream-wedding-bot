"""Module contains class for form response data getter."""


from entities.schemas.commands import CommandSchema
from entities.schemas.forms import GuestFormSchema
from exceptions.repositories import ObjectNotFoundException
from exceptions.use_cases import CommandNotFoundException
from services.messages.getters.base import BaseMessageDataGetter
from typings.services import MessageFactoryDataTuple


class FormResponseDataGetter(BaseMessageDataGetter[
    MessageFactoryDataTuple[CommandSchema[str | None]],
]):
    """Form response data service."""

    async def __call__(
        self,
        *,
        guest_form: GuestFormSchema,
    ) -> MessageFactoryDataTuple[CommandSchema[str | None]]:
        """Get form response base data.

        :param guest_form: Guest form schema.
        :return: MessageSchema, list of CommandSchema.
        """
        form_stage = guest_form.stage

        try:
            callback_message = await self._callback_message_repository.get_by_form_stage(form_stage)
        except ObjectNotFoundException as exc:
            raise CommandNotFoundException from exc

        available_commands = [
            _
            async for _ in self._command_repository.filter_by_form_stage(form_stage=form_stage)
        ]

        return MessageFactoryDataTuple(
            message_ref=callback_message,
            commands=available_commands,
        )