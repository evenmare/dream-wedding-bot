"""Module contains invitations schemas implementations."""

from pydantic import BaseModel, Field

from entities.enums.forms import GuestFormStageEnum


class GuestFormSchema(BaseModel):
    """Invitation request schema."""

    guest_id: int
    stage: GuestFormStageEnum
    additional_info: str | None = Field(default=None)
