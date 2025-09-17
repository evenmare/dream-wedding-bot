"""Module contains logic for accessing callback messages info."""

from tortoise.exceptions import DoesNotExist

from entities.database.callbacks import CallbackMessage
from entities.enums.initial_commands import InitialCommandEnum
from entities.schemas.callbacks import MessageReferenceSchema
from exceptions.repositories import ObjectNotFoundException
from repositories.database.base import BaseDatabaseRepository
from entities.enums.forms import GuestFormStageEnum


class CallbackMessageRepository(BaseDatabaseRepository[CallbackMessage, MessageReferenceSchema]):
    """Class contains callback messages access repository."""

    schema = MessageReferenceSchema
    _model = CallbackMessage

    async def get_by_initial_command(
        self,
        initial_command: InitialCommandEnum,
    ) -> MessageReferenceSchema:
        """Method returns callback message schema for initial commands.

        :param initial_command: Initial command.
        :return: Callback message schema.
        """
        try:
            callback_orm = await self._model.get(initial_command=initial_command)
        except DoesNotExist as exc:
            raise ObjectNotFoundException(f'message from initial_command={initial_command}') from exc

        return self._serialize_model(callback_orm)

    async def get_by_form_stage(
        self,
        form_stage: GuestFormStageEnum,
    ) -> MessageReferenceSchema:
        """Method returns callback message schema for guest form stage.

        :param form_stage: Form filling stage.
        :raises ObjectNotFoundException:  If callback message not found.
        :return: Callback message schema.
        """
        try:
            callback_orm = await self._model.get(form_stage=form_stage)
        except DoesNotExist as exc:
            raise ObjectNotFoundException(f'message from form_stage={form_stage}') from exc

        return self._serialize_model(callback_orm)

    async def get_by_command_id(
        self,
        command_id: int,
    ) -> MessageReferenceSchema:
        """Method returns callback message schema for command.

        :param command_id: Command identity.
        :raises ObjectNotFoundException: If callback message not found.
        :return: Callback message schema.
        """
        try:
            callback_orm = await self._model.get(command_id=command_id)
        except DoesNotExist as exc:
            raise ObjectNotFoundException(f'message from command_id={command_id}') from exc

        return self._serialize_model(callback_orm)

    async def get_by_notification_id(
        self,
        notification_id: int,
    ) -> MessageReferenceSchema:
        """Method returns callback message schema for notification.

        :param notification_id: Notification identity.
        :return: Callback message schema.
        """
        try:
            callback_orm = await self._model.get(notification_id=notification_id)
        except DoesNotExist as exc:
            raise ObjectNotFoundException(f'message from notification_id={notification_id}') from exc

        return self._serialize_model(callback_orm)
