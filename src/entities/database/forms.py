"""Module contains guests models implementations."""

from tortoise import fields

from entities.database.base import BaseOrmModel
from entities.enums.forms import GuestFormStageEnum


class GuestForm(BaseOrmModel):
    """Guest form information."""

    guest = fields.OneToOneField(
        model_name='dream_wedding_bot.Guest',
        related_name='form',
        on_delete=fields.OnDelete.RESTRICT,
        pk=True,
    )

    stage = fields.CharEnumField(
        GuestFormStageEnum,
        max_length=32,
        null=False,
    )

    class Meta:
        table = 'guests_forms'
