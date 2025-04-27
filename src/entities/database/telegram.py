"""Module contains implementations of Telegram models."""

from tortoise import fields

from entities.database.base import BaseOrmModel


class TelegramUser(BaseOrmModel):
    """Telegram user model."""

    id = fields.IntField(
        primary_key=True,
        generated=False,
    )
    username = fields.CharField(
        max_length=64,
        null=True,
    )

    guest = fields.OneToOneField(
        model_name='dream_wedding_bot.Guest',
        related_name='telegram_user',
    )

    class Meta:
        table = 'telegram_users'
