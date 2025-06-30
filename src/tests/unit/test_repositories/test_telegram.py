"""Module contains tests for Telegram user repository."""

import pytest

from entities.database.guests import Guest
from entities.database.telegram import TelegramUser
from entities.schemas.telegram import TelegramUserSchema
from repositories.database.telegram import TelegramUserRepository

pytestmark = pytest.mark.usefixtures(
    'db',
)


async def test_create_telegram_user(guests: list[Guest]):
    """Validate Telegram user creation."""
    telegram_user_repository = TelegramUserRepository()

    input_schema = TelegramUserSchema(
        user_id=1,
        username='test_user',
    )

    guest_id = guests[0].guest_id
    output_schema = await telegram_user_repository.update_or_create_by_guest_id(
        guest_id=guest_id,
        telegram_user=input_schema,
    )

    assert input_schema == output_schema

    user_orm = await TelegramUser.get(guest_id=guest_id)
    assert user_orm.user_id == input_schema.user_id
    assert user_orm.username == input_schema.username

    assert await TelegramUser.all().count() == 1


async def test_update_telegram_user(guests: list[Guest]) -> None:
    """Validate Telegram user update."""
    telegram_user_repository = TelegramUserRepository()

    input_schema = TelegramUserSchema(
        user_id=1,
        username='test_user',
    )

    guest_id = guests[0].guest_id

    # Create Telegram user
    await telegram_user_repository.update_or_create_by_guest_id(
        guest_id=guest_id,
        telegram_user=input_schema,
    )

    user_orm = await TelegramUser.get(guest_id=guest_id)
    last_updated_at = user_orm.updated_at

    # Update Telegram user
    input_schema.username = 'new_username'
    output_schema = await telegram_user_repository.update_or_create_by_guest_id(
        guest_id=guest_id,
        telegram_user=input_schema,
    )

    assert input_schema == output_schema

    await user_orm.refresh_from_db()

    assert user_orm.updated_at > last_updated_at
    assert user_orm.user_id == input_schema.user_id
    assert user_orm.username == input_schema.username
