"""Module contains tests for CallbackMessage repository."""

import pytest

from entities.database.callback_messages import CallbackMessage
from entities.enums.commands import CommandEnum
from entities.enums.forms import GuestFormStageEnum
from entities.schemas.messages import MessageReferenceSchema
from repositories.database.callback_messages import CallbackMessageRepository


pytestmark = pytest.mark.usefixtures(
    'db',
)


async def test_get_callback_by_command(callback_messages: list[CallbackMessage]):
    """Validate retrieve callback message by command."""
    callback_message_repository = CallbackMessageRepository()

    callback_message_orm = callback_messages[1]
    callback_message_schema = await callback_message_repository.get_callback_by_command(
        command=CommandEnum.START,
    )

    _assert_schema_eq_record(callback_message_schema, callback_message_orm)


async def test_get_callback_by_command__not_found():
    """Validate retrieve callback message by command if does not exist."""
    callback_message_repository = CallbackMessageRepository()
    assert not await callback_message_repository.get_callback_by_command(
        command=CommandEnum.START
    )


async def test_get_callback_by_form_stage(callback_messages: list[CallbackMessage]):
    """Validate retrieve callback message by form stage."""
    callback_message_repository = CallbackMessageRepository()

    callback_message_orm = callback_messages[0]
    callback_message_schema = (
        await callback_message_repository.get_callback_by_form_stage(
            form_stage=GuestFormStageEnum.AWAITING_ANSWER,
        )
    )

    _assert_schema_eq_record(callback_message_schema, callback_message_orm)


def _assert_schema_eq_record(
    schema: MessageReferenceSchema, orm_record: CallbackMessage
) -> None:
    """Assert schema contains data of needed record."""
    assert schema.text_filepath == orm_record.text_filepath
    assert schema.image_filepath == orm_record.image_filepath
