"""Module contains implementations of invitation models."""

from typing import TYPE_CHECKING
from tortoise import fields

from entities.database.base import BaseOrmModel

if TYPE_CHECKING:
    from entities.database.guests import Guest


class InvitationRequest(BaseOrmModel):
    """Invitation request model."""

    guest: fields.OneToOneRelation['Guest'] = fields.OneToOneField(
        model_name='dream_wedding_bot.Guest',
        related_name='invitation_request',
        on_delete=fields.OnDelete.RESTRICT,
        primary_key=True,
    )

    address = fields.TextField(null=True)
    address_specification = fields.TextField(null=True)

    class Meta:
        table = 'invitations_requests'
