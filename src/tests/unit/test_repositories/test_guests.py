"""Module contains tests of guests repository."""

import pytest

from entities.database.guests import Guest
from entities.database.telegram import TelegramUser
from entities.schemas.guests import GuestSchema
from exceptions.repositories import ObjectNotFoundException
from repositories.database.guests import GuestRepository

pytestmark = pytest.mark.usefixtures(
    'db',
)


async def test_get_by_guest_id(guests: list[Guest]):
    """Validate retrieve guest record by id."""
    guest_repository = GuestRepository()

    guest_orm = guests[0]
    guest_schema = await guest_repository.get_by_guest_id(guest_id=guest_orm.guest_id)

    _assert_schema_eq_record(guest_schema, guest_orm)


async def test_get_by_guest_id__guest_not_found():
    """Validate retrieve guest record by id if record not exists."""
    guest_repository = GuestRepository()

    with pytest.raises(ObjectNotFoundException) as exc_info:
        await guest_repository.get_by_guest_id(guest_id=0)

    assert repr(exc_info.value) == 'Object Not Found: Guest with guest_id=0'


@pytest.mark.usefixtures('telegram_users')
async def test_get_by_telegram_user_id(guests: list[Guest]):
    """Validate retrieve guest record by telegram user id."""
    guest_repository = GuestRepository()

    guest_orm = guests[0]
    user_orm: TelegramUser = await guest_orm.telegram_user
    assert user_orm

    guest_schema = await guest_repository.get_by_telegram_user_id(
        user_id=user_orm.user_id
    )

    _assert_schema_eq_record(guest_schema, guest_orm)


@pytest.mark.usefixtures('telegram_users')
async def test_get_by_telegram_user_id__guest_not_found():
    """Validate retrieve guest record by telegram user id if record not exists."""
    guest_repository = GuestRepository()

    with pytest.raises(ObjectNotFoundException) as exc_info:
        await guest_repository.get_by_telegram_user_id(user_id=0)

    assert repr(exc_info.value) == 'Object Not Found: Guest with telegram user_id=0'


@pytest.mark.parametrize(
    'slice_indices',
    [
        pytest.param(
            (),
            id='no_guests',
        ),
        pytest.param(
            (0, 1),
            id='one_guest',
        ),
        pytest.param(
            (0, 2),
            id='two_guests',
        ),
    ],
)
async def test_filter_all_by_guests_ids(
    guests: list[Guest], slice_indices: tuple[int, ...]
):
    """Validate retrieve guest generator by guests ids."""
    guest_repository = GuestRepository()

    expected_guests_orm_list: list[Guest] = []
    guests_ids: list[int] = []
    if slice_indices:
        expected_guests_orm_list = guests[slice(*slice_indices)]
        guests_ids = [guest_orm.guest_id for guest_orm in expected_guests_orm_list]

    retrieved_guests_list: list[GuestSchema] = []

    async for guest_orm in guest_repository.filter_all_by_guests_id(
        guests_ids=guests_ids
    ):
        retrieved_guests_list.append(guest_orm)

    assert len(retrieved_guests_list) == len(expected_guests_orm_list)
    for retrieved_guest_schema, expected_guest_orm in zip(
        retrieved_guests_list,
        expected_guests_orm_list,
        strict=True,
    ):
        _assert_schema_eq_record(retrieved_guest_schema, expected_guest_orm)


async def test_filter_by_phone_number(guests: list[Guest]):
    """Validate filters on guests."""
    guest_repository = GuestRepository()

    existing_guest: Guest = guests[0]
    guest_schema = await guest_repository.filter_by_phone_number(
        phone_number=existing_guest.phone_number,
    )

    assert guest_schema
    assert guest_schema.phone_number == existing_guest.phone_number

    not_existing_phone_number = '0'
    assert not await guest_repository.filter_by_phone_number(
        phone_number=not_existing_phone_number
    )


def _assert_schema_eq_record(schema: GuestSchema, orm_record: Guest) -> None:
    """Assert schema contains data of needed record."""
    assert schema.first_name == orm_record.first_name
    assert schema.last_name == orm_record.last_name
    assert schema.patronymic == orm_record.patronymic
    assert schema.phone_number == orm_record.phone_number
    assert schema.birth_date == orm_record.birth_date
    assert schema.gender == orm_record.gender
    assert schema.category == orm_record.category
    assert schema.is_resident == orm_record.is_resident
    assert schema.is_registration_guest == orm_record.is_registration_guest
