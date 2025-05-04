"""Module contains models for callback messages store."""

from tortoise import fields

from entities.database.base import BaseOrmModel
from entities.enums.commands import CommandEnum
from entities.enums.forms import GuestFormStageEnum


class CallbackMessage(BaseOrmModel):
    """Model for storing message content for callbacks."""

    callback_message_id = fields.IntField(
        primary_key=True,
        generated=True,
    )

    form_stage = fields.CharEnumField(
        GuestFormStageEnum,
        max_length=32,
        null=True,
    )
    command = fields.CharEnumField(
        CommandEnum,
        max_length=32,
        null=True,
    )

    text_filepath = fields.CharField(
        max_length=64,
        null=False,
    )
    image_filepath = fields.CharField(
        max_length=64,
        null=True,
    )

    class Meta:
        table = 'callback_messages'
