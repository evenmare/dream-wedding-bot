"""Module contains callback messages initial data."""

from collections.abc import AsyncGenerator

import pytest

from entities.database.callback_messages import CallbackMessage
from entities.enums.commands import CommandEnum
from entities.enums.forms import GuestFormStageEnum


def _generate_callback_messages() -> list[CallbackMessage]:
    """Generates list of callback messages."""
    return [
        CallbackMessage(
            form_stage=GuestFormStageEnum.AWAITING_ANSWER,
            text_filepath='text.html',
        ),
        CallbackMessage(
            command=CommandEnum.START,
            text_filepath='start.html',
            image_filepath='image.png',
        ),
    ]


@pytest.fixture(scope='function')
async def callback_messages(db: AsyncGenerator[None, None]) -> list[CallbackMessage]:
    """Creates callback messages list."""
    callback_messages_orm = _generate_callback_messages()
    await CallbackMessage.bulk_create(callback_messages_orm)
    return list(await CallbackMessage.all())
