"""Module contains test data for Guest entity."""

from collections.abc import AsyncGenerator
import datetime

import pytest

from entities.database.guests import Guest
from entities.enums.guests import GuestCategoryEnum, GuestGenderEnum


def _generate_guests() -> list[Guest]:
    """Generates list of guests."""
    return [
        Guest(
            first_name='Kirill',
            last_name='Vershinin',
            patronymic='Alexandrovich',
            phone_number='+79999999999',
            birth_date=datetime.date(2001, 12, 29),
            gender=GuestGenderEnum.MALE,
            category=GuestCategoryEnum.NEWLYWEDS,
            is_resident=True,
            is_registration_guest=True,
        ),
        Guest(
            first_name='Some',
            last_name='Guest',
            patronymic='Guestovich',
            phone_number='+79888888888',
            birth_date=datetime.date(2000, 1, 1),
            gender=GuestGenderEnum.FEMALE,
            category=GuestCategoryEnum.FRIEND,
            is_resident=False,
            is_registration_guest=False,
        ),
    ]


@pytest.fixture(scope='function')
async def guests(db: AsyncGenerator[None, None]) -> list[Guest]:
    """Creates guests list."""
    guests_orm = _generate_guests()
    await Guest.bulk_create(guests_orm)
    return list(await Guest.all())
