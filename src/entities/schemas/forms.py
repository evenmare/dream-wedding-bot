"""Module contains invitations schemas implementations."""

from pydantic import BaseModel

from entities.enums.forms import GuestFormStageEnum


class GuestFormSchema(BaseModel):
    """Invitation request schema."""

    guest_id: int
    stage: GuestFormStageEnum
