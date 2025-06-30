"""Module contains commands access repositories."""

from entities.database.commands import AvailableCommand, Command
from entities.enums.forms import GuestFormStageEnum
from entities.enums.initial_commands import InitialCommandEnum
from entities.schemas.commands import CommandSchema
from exceptions.repositories import ObjectNotFoundException
from repositories.database.base import BaseManyToManyRepository

from tortoise.exceptions import DoesNotExist
from tortoise.expressions import Q

from typing import AsyncGenerator


class CommandRepository(BaseManyToManyRepository[Command, AvailableCommand, CommandSchema]):
    """Class implements command access repository."""

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
        :return: Async generator of commands.
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

        :param guest_command_pairs: Guest-Command identificators pair.
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
