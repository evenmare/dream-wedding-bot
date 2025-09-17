"""Module contains models for notifications."""

from typing import TYPE_CHECKING
from tortoise import fields

from entities.database.base import BaseOrmModel

if TYPE_CHECKING:
    from entities.database.guests import Guest


class Notification(BaseOrmModel):
    """Model for storing notification info."""

    notification_id = fields.IntField(
        primary_key=True,
        generated=True,
    )

    code = fields.CharField(
        max_length=16,
        null=False,
        unique=True,
    )

    is_personal = fields.BooleanField(default=True)

    guests: fields.ManyToManyRelation['Guest'] = fields.ManyToManyField(
        model_name='dream_wedding_bot.Guest',
        through='personal_notifications',
        forward_key='guest_id',
        backward_key='notification_id',
        related_name='personal_notifications',
    )

    class Meta:
        table = 'notifications'


class PersonalNotification(BaseOrmModel):
    """Model for storing available notifications for Guest."""

    guest: fields.ForeignKeyRelation['Guest'] = fields.ForeignKeyField(
        model_name='dream_wedding_bot.Guest',
        on_delete=fields.CASCADE,
    )
    notification: fields.ForeignKeyRelation['Notification'] = fields.ForeignKeyField(
        model_name='dream_wedding_bot.Notification',
        on_delate=fields.CASCADE,
        related_name='personal_notification',
    )

    is_sent = fields.BooleanField(default=False)

    class Meta:
        table = 'personal_notifications'
