"""Module contains implementations of Telegram models."""

from typing import TYPE_CHECKING
from tortoise import fields

from entities.database.base import BaseOrmModel

if TYPE_CHECKING:
    from entities.database.guests import Guest


class TelegramUser(BaseOrmModel):
    """Telegram user model."""

    user_id = fields.BigIntField(
        primary_key=True,
        generated=False,
    )
    username = fields.CharField(
        max_length=64,
        null=True,
    )

    guest: fields.OneToOneRelation['Guest'] = fields.OneToOneField(
        model_name='dream_wedding_bot.Guest',
        related_name='telegram_user',
        on_delete=fields.OnDelete.CASCADE,
        null=False,
    )

    class Meta:
        table = 'telegram_users'
