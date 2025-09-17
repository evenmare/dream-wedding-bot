"""Module contains test data for GuestForm entity."""

from collections.abc import AsyncGenerator

import pytest

from entities.database.guests import Guest
from entities.database.forms import GuestForm
from entities.enums.forms import GuestFormStageEnum


def _generate_guest_forms(guests: list[Guest]) -> list[GuestForm]:
    """Generates list of guests forms."""
    return [
        GuestForm(
            stage=GuestFormStageEnum.AWAITING_ANSWER,
            guest=guests[0],
        ),
        GuestForm(
            stage=GuestFormStageEnum.COMPLETED,
            guest=guests[1],
        ),
    ]


@pytest.fixture(scope='function')
async def guest_forms(
    db: AsyncGenerator[None, None],
    guests: list[Guest],
):
    """Creates guests forms list."""
    guest_forms_orm = _generate_guest_forms(guests=guests)
    await GuestForm.bulk_create(guest_forms_orm)
    return list(await GuestForm.all())
