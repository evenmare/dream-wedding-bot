"""Module contains logic for accessing callback messages info."""

from entities.database.callback_messages import CallbackMessage
from entities.enums.commands import CommandEnum
from entities.schemas.messages import MessageReferenceSchema
from repositories.database.base import BaseDatabaseRepository
from entities.enums.forms import GuestFormStageEnum


class CallbackMessageRepository(
    BaseDatabaseRepository[CallbackMessage, MessageReferenceSchema]
):
    """Class contains callback messages access repository."""

    schema = MessageReferenceSchema
    _model = CallbackMessage

    async def get_callback_by_command(
        self,
        command: CommandEnum,
    ) -> MessageReferenceSchema | None:
        """Method returns callback message schema for command if exists.

        :param command: Command.
        :return: Callback message schema if exists.
        """
        callback_orm = await self._model.get_or_none(command=command)

        if not callback_orm:
            return None

        return self._serialize_model(callback_orm)

    async def get_callback_by_form_stage(
        self,
        form_stage: GuestFormStageEnum,
    ) -> MessageReferenceSchema:
        """Method returns callback message schema for guest form stage.

        :param form_stage: Form filling stage.
        :return: Callback message schema.
        """
        callback_orm = await self._model.get(form_stage=form_stage)
        return self._serialize_model(callback_orm)
