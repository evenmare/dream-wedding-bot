"""Module contains implementations of invitation models."""

from tortoise import fields

from entities.database.base import BaseOrmModel


class InvitationRequest(BaseOrmModel):
    """Invitation request model."""

    guest = fields.OneToOneField(
        model_name='dream_wedding_bot.Guest',
        related_name='invitation_request',
        on_delete=fields.OnDelete.RESTRICT,
        pk=True,
    )

    address = fields.TextField(null=True)
    address_specification = fields.TextField(null=True)

    class Meta:
        table = 'invitations_requests'
