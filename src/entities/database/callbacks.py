"""Module contains models for callback messages store."""

from typing import TYPE_CHECKING
from tortoise import fields

from entities.database.base import BaseOrmModel
from entities.enums.forms import GuestFormStageEnum
from entities.enums.initial_commands import InitialCommandEnum

if TYPE_CHECKING:
    from entities.database.commands import Command
    from entities.database.notifications import Notification


class CallbackMessage(BaseOrmModel):
    """Model for storing message content for callbacks."""

    callback_message_id = fields.IntField(
        primary_key=True,
        generated=True,
    )

    initial_command: InitialCommandEnum = fields.CharEnumField(
        enum_type=InitialCommandEnum,
        max_length=32,
        null=True,
    )
    form_stage: GuestFormStageEnum = fields.CharEnumField(
        enum_type=GuestFormStageEnum,
        max_length=32,
        null=True,
    )
    command: fields.OneToOneNullableRelation['Command'] = fields.OneToOneField(
        model_name='dream_wedding_bot.Command',
        related_name='message',
        on_delete=fields.OnDelete.RESTRICT,
        null=True,
    )
    notification: fields.OneToOneNullableRelation['Notification'] = fields.OneToOneField(
        model_name='dream_wedding_bot.Notification',
        related_name='notification',
        on_delete=fields.OnDelete.SET_NULL,
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

    required_data = fields.JSONField(
        default=None,
        null=True,
    )

    class Meta:
        table = 'callback_messages'
