"""Module contains guest schemas implementations."""

import datetime

from pydantic import BaseModel

from entities.enums.guests import GuestCategoryEnum, GuestGenderEnum


class GuestSchema(BaseModel):
    """Schema for guest."""

    guest_id: int
    first_name: str
    last_name: str
    patronymic: str | None
    phone_number: str
    birth_date: datetime.date
    gender: GuestGenderEnum
    category: GuestCategoryEnum
    is_resident: bool
    is_registration_guest: bool
    updated_at: datetime.datetime
