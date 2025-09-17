"""Module contains test data for TelegramUser entity."""

from collections.abc import AsyncGenerator

import pytest

from entities.database.guests import Guest
from entities.database.telegram import TelegramUser


def _generate_telegram_users(guests: list[Guest]) -> list[TelegramUser]:
    """Generates list of telegram users."""
    return [
        TelegramUser(
            user_id=90001,
            username='evenmare',
            guest=guests[0],
        ),
        TelegramUser(
            user_id=90002,
            username='test_user',
            guest=guests[1],
        ),
    ]


@pytest.fixture(scope='function')
async def telegram_users(
    db: AsyncGenerator[None, None],
    guests: list[Guest],
) -> list[TelegramUser]:
    """Creates telegram users list."""
    users_orm = _generate_telegram_users(guests=guests)
    await TelegramUser.bulk_create(users_orm)
    return list(await TelegramUser.all())
