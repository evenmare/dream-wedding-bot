"""Module contains invitations schemas implementations."""

from pydantic import BaseModel

from entities.enums.invitations import InvitationRequestStageEnum


class InvitationRequestSchema(BaseModel):
    """Invitation request schema."""

    stage: InvitationRequestStageEnum
    address: str
    address_specification: str
    guest_id: int
