"""Module contains implementations of invitation models."""

from tortoise import fields

from entities.database.base import BaseOrmModel
from entities.enums.invitations import InvitationRequestStageEnum


class InvitationRequest(BaseOrmModel):
    """Invitation request model."""

    stage = fields.CharEnumField(
        InvitationRequestStageEnum,
        null=False,
        max_length=32,
    )

    address = fields.TextField(null=True)
    address_specification = fields.TextField(null=True)

    guest = fields.OneToOneField(
        model_name="dream_wedding_bot.Guest",
        related_name="invitation_request",
    )

    class Meta:
        table = "invitations_requests"
