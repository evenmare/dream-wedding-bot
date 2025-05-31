"""Module contains callback messages initial data."""

from collections.abc import AsyncGenerator

import pytest

from entities.database.callbacks import AvailableCommand, CallbackMessage, Command
from entities.database.guests import Guest
from entities.enums.entities import ContextEntityEnum
from entities.enums.forms import GuestFormStageEnum


def _generate_commands() -> list[Command]:
    """Generates list of commands."""
    return [
        Command(
            text='Text',
            form_stage=GuestFormStageEnum.AWAITING_ANSWER,
            is_restricted=False,
        ),
        Command(
            text='No text',
            code='Code',
            is_restricted=True,
        ),
        Command(
            text='Text',
            code='Code',
            is_restricted=False,
        )
    ]


def _generate_callback_messages(commands_orm: list[Command]) -> list[CallbackMessage]:
    """Generates list of callback messages."""
    return [
        CallbackMessage(
            form_stage=GuestFormStageEnum.AWAITING_ANSWER,
            text_filepath='text.html',
            required_data={ContextEntityEnum.GUEST: ['last_name', 'first_name']},
        ),
        CallbackMessage(
            text_filepath='start.html',
            image_filepath='image.png',
            command=commands_orm[1],
        ),
    ]


@pytest.fixture(scope='function')
async def commands(db: AsyncGenerator[None, None], guests: list[Guest]) -> list[Command]:
    """Creates commands list."""
    commands_orm = _generate_commands()
    await Command.bulk_create(commands_orm)

    commands_orm = list(await Command.all())

    await AvailableCommand.create(
        guest=guests[0],
        command=commands_orm[1],
    )

    return commands_orm


@pytest.fixture(scope='function')
async def callback_messages(db: AsyncGenerator[None, None], commands: list[Command]) -> list[CallbackMessage]:
    """Creates callback messages list."""
    callback_messages_orm = _generate_callback_messages(commands)
    await CallbackMessage.bulk_create(callback_messages_orm)
    return list(await CallbackMessage.all())
