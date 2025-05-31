"""Module contains models for callback messages store."""

from typing import TYPE_CHECKING
from tortoise import fields

from entities.database.base import BaseOrmModel
from entities.enums.forms import GuestFormStageEnum
from entities.enums.initial_commands import InitialCommandEnum

if TYPE_CHECKING:
    from entities.database.guests import Guest


class Command(BaseOrmModel):
    """Model for storing all available commands."""

    command_id = fields.IntField(
        primary_key=True,
        generated=True,
    )

    text = fields.CharField(max_length=64)
    code = fields.CharField(
        max_length=16,
        null=True,
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

    is_restricted = fields.BooleanField(default=True)
    is_negative_feedback = fields.BooleanField(default=False)

    guests: fields.ManyToManyRelation['Guest'] = fields.ManyToManyField(
        model_name='dream_wedding_bot.Guest',
        through='available_commands',
        forward_key='guest_id',
        backward_key='command_id',
        related_name='available_commands',
    )

    class Meta:
        table = 'commands'


class AvailableCommand(BaseOrmModel):
    """Model for storing available commands for Guest."""

    guest: fields.ForeignKeyRelation['Guest'] = fields.ForeignKeyField(
        model_name='dream_wedding_bot.Guest',
        on_delete=fields.CASCADE,
    )
    command: fields.ForeignKeyRelation['Command'] = fields.ForeignKeyField(
        model_name='dream_wedding_bot.Command',
        related_name='link_guest',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'available_commands'


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
