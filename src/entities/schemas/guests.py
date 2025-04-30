"""Module contains guest schemas implementations."""

import datetime

from pydantic import BaseModel

from entities.enums.guests import GuestCategoryEnum


class GuestSchema(BaseModel):
    """Schema for guest."""

    first_name: str
    last_name: str
    patronymic: str
    phone_number: str
    birth_date: datetime.date
    gender: str
    category: GuestCategoryEnum
    is_resident: bool
    is_registration_guest: bool
