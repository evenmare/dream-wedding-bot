"""Module contains tests for CallbackMessage repository."""

import pytest

from entities.database.callbacks import AvailableCommand, CallbackMessage, Command
from entities.database.guests import Guest
from entities.enums.forms import GuestFormStageEnum
from entities.schemas.callbacks import CommandSchema, MessageReferenceSchema
from repositories.database.callbacks import CallbackMessageRepository, CommandRepository


pytestmark = pytest.mark.usefixtures(
    'db',
)


async def test_get_available_command_by_code(
    guests: list[Guest],
    commands: list[Command],
):
    """Validate retrieve available command by code."""
    command_repository = CommandRepository()

    command_orm = commands[1]
    command_schema = await command_repository.get_available_by_code(
        guest_id=guests[0].guest_id,
        code='Code',
    )

    _assert_command_schema_eq_record(command_schema, command_orm)


async def test_get_command_by_form_stage(commands: list[Command]):
    """Validate retrieve command by form stage."""
    command_repository = CommandRepository()

    command_orm = commands[0]
    command_schema = await command_repository.filter_by_form_stage(form_stage=GuestFormStageEnum.AWAITING_ANSWER)

    _assert_command_schema_eq_record(command_schema, command_orm)


async def test_filter_all_for_personalization(commands: list[Command]):
    """Validate retrieve commands without form stage link with no restrictions."""
    command_repository = CommandRepository()

    expected_command_orm = commands[2]

    generator = command_repository.filter_available()

    command_schema = await anext(generator)
    _assert_command_schema_eq_record(command_schema, expected_command_orm)

    with pytest.raises(StopAsyncIteration):
        await anext(generator)


async def test_filter_all_for_personalization__by_guest(commands: list[Command], guests: list[Guest]):
    """Validate retrieve available commands for guest."""
    command_repository = CommandRepository()

    guest_orm = guests[0]
    expected_command_orm = commands[1]

    generator = command_repository.filter_available(guest_id=guest_orm.guest_id)

    command_schema = await anext(generator)
    _assert_command_schema_eq_record(command_schema, expected_command_orm)

    with pytest.raises(StopAsyncIteration):
        await anext(generator)


async def test_make_available_command_for_guest(
    guests: list[Guest],
    commands: list[Command],
):
    """Validate make command as allowed for guest."""
    command_repository = CommandRepository()

    command_orm = commands[1]
    guest_orm = guests[1]

    await command_repository.make_available_for_guest(
        guest_id=guest_orm.guest_id,
        commands_ids=frozenset((command_orm.command_id,)),
    )

    await AvailableCommand.get(
        command_id=command_orm.command_id,
        guest_id=guest_orm.guest_id,
    )


async def test_get_callback_by_command(callback_messages: list[CallbackMessage]):
    """Validate retrieve callback message by command."""
    callback_message_repository = CallbackMessageRepository()

    callback_message_orm = callback_messages[1]
    callback_message_schema = await callback_message_repository.get_by_command(
        command_id=callback_messages[1].command_id,
    )

    _assert_callback_message_schema_eq_record(callback_message_schema, callback_message_orm)


async def test_get_callback_by_command__not_found():
    """Validate retrieve callback message by command if does not exist."""
    callback_message_repository = CallbackMessageRepository()
    assert not await callback_message_repository.get_by_command(command_id=-1)


async def test_get_callback_by_form_stage(callback_messages: list[CallbackMessage]):
    """Validate retrieve callback message by form stage."""
    callback_message_repository = CallbackMessageRepository()

    callback_message_orm = callback_messages[0]
    callback_message_schema = await callback_message_repository.get_by_form_stage(
        form_stage=GuestFormStageEnum.AWAITING_ANSWER,
    )

    _assert_callback_message_schema_eq_record(callback_message_schema, callback_message_orm)


def _assert_command_schema_eq_record(
    schema: CommandSchema,
    orm_record: Command,
) -> None:
    """Assert command schema contains data of needed recod."""
    assert schema.command_id == orm_record.command_id
    assert schema.text == orm_record.text
    assert schema.code == orm_record.code


def _assert_callback_message_schema_eq_record(
    schema: MessageReferenceSchema,
    orm_record: CallbackMessage,
) -> None:
    """Assert message schema contains data of needed record."""
    assert schema.text_filepath == orm_record.text_filepath
    assert schema.image_filepath == orm_record.image_filepath
    assert schema.required_data == orm_record.required_data
