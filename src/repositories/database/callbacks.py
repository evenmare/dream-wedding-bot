"""Module contains logic for accessing callback messages info."""

from typing import AsyncGenerator
from tortoise.expressions import Q
from tortoise.exceptions import DoesNotExist

from entities.database.callbacks import AvailableCommand, CallbackMessage, Command
from entities.enums.initial_commands import InitialCommandEnum
from entities.schemas.callbacks import CommandSchema, MessageReferenceSchema
from exceptions.repositories import ObjectNotFoundException
from repositories.database.base import BaseDatabaseRepository
from entities.enums.forms import GuestFormStageEnum


class CommandRepository(BaseDatabaseRepository[Command, CommandSchema]):
    """Class contains command access repository."""

    schema = CommandSchema
    _model = Command
    _m2m_model = AvailableCommand

    async def get_available_by_code[_CodeType = str](
        self,
        guest_id: int,
        code: str,
    ) -> CommandSchema[_CodeType]:
        """Method returns available command by code.

        :param guest_id: Guest identificator.
        :param code: Callback code.
        :raises ObjectNotFoundException: If command not found by code.
        :return: Command schema.
        """
        try:
            command_orm = await self._model.get(
                Q(guests__guest_id=guest_id) | Q(link_guest__isnull=True),
                code=code,
            )
        except DoesNotExist as exc:
            raise ObjectNotFoundException(f'command by guest_id={guest_id} code={code}') from exc

        return self._serialize_model(command_orm, code_type=str)

    async def filter_by_form_stage[_CodeType = str | None](
        self,
        form_stage: GuestFormStageEnum,
    ) -> AsyncGenerator[CommandSchema[_CodeType], None]:
        """Method returns commands async generator by form stage.

        :param form_stage: Form stage.
        :return: Command schema.
        """
        query = self._model.filter(form_stage=form_stage).order_by('is_negative_feedback')

        async for command_orm in aiter(query):
            yield self._serialize_model(command_orm, code_type=str | None)

    async def filter_by_initial_command[_CodeType = str | None](
        self,
        initial_command: InitialCommandEnum,
    ) -> AsyncGenerator[CommandSchema[_CodeType], None]:
        """Method returns commands async generator by initial command.

        :param initial_command: Initial command.
        :return: Command schema.
        """
        query = self._model.filter(initial_command=initial_command)

        async for command_orm in aiter(query):
            yield self._serialize_model(command_orm, code_type=str | None)

    async def filter_available[_CodeType = str](
        self,
        guest_id: int | None = None,
    ) -> AsyncGenerator[CommandSchema[_CodeType], None]:
        """Method returns all commands for personaliation.

        :param guest_id: Guest identificator.
        :return: List of commands.
        """
        query = self._model.filter(
            initial_command__isnull=True,
            form_stage__isnull=True,
        ).order_by('created_at')

        if guest_id:
            query = query.filter(guests__guest_id=guest_id)
        else:
            query = query.filter(is_restricted=False)

        commands_iterator = aiter(query)

        async for command_orm in commands_iterator:
            yield self._serialize_model(command_orm, code_type=str)

    async def make_available_for_guests[_GuestId = int, _CommandId = int](
        self,
        guest_command_pairs: frozenset[tuple[_GuestId, _CommandId]],
    ) -> None:
        """Method makes commands available for guests.

        :param guest_id: Guest identificator.
        :param commands_ids: Commands identificators.
        """
        available_commands_orm: list[AvailableCommand] = [
            AvailableCommand(
                guest_id=guest_id,
                command_id=command_id,
            )
            for guest_id, command_id in guest_command_pairs
        ]

        await self._m2m_model.bulk_create(available_commands_orm)

    def _serialize_model[_CodeType](self, obj_orm: Command, *, code_type: _CodeType) -> CommandSchema[_CodeType]:
        """Method implements logic for serializing a model record."""
        return CommandSchema[code_type].model_validate(
            obj_orm,
            from_attributes=True,
        )


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

    async def get_by_command(
        self,
        command_id: int,
    ) -> MessageReferenceSchema:
        """Method returns callback message schema for command if exists.

        :param command: Command.
        :raises ObjectNotFoundException: If callback message not found.
        :return: Callback message schema if exists.
        """
        try:
            callback_orm = await self._model.get(command_id=command_id)
        except DoesNotExist as exc:
            raise ObjectNotFoundException(f'message from command_id={command_id}') from exc

        return self._serialize_model(callback_orm)
