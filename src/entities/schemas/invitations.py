"""Module contains invitations schemas implementations."""

from pydantic import BaseModel, Field


class InvitationRequestSchema(BaseModel):
    """Invitation request schema."""

    guest_id: int
    address: str | None = Field(default=None)
    address_specification: str | None = Field(default=None)
