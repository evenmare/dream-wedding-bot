"""Module contains guests forms repositories tests."""

import pytest

from entities.database.forms import GuestForm
from entities.database.guests import Guest
from entities.enums.forms import GuestFormStageEnum
from entities.schemas.forms import GuestFormSchema
from exceptions.repositories import IntegrityError, ObjectNotFoundException
from repositories.database.forms import GuestFormRepository

pytestmark = pytest.mark.usefixtures(
    'db',
)


async def test_get_form_by_guest_id(
    guests: list[Guest],
    guest_forms: list[GuestForm],
):
    """Validate retrieve guest form by guest_id."""
    guest_form_repository = GuestFormRepository()

    guest_form_orm = guest_forms[0]
    guest_orm = guests[0]

    assert guest_form_orm.guest_id == guest_orm.guest_id

    guest_form_schema = await guest_form_repository.get_by_guest_id(
        guest_id=guest_orm.guest_id
    )
    _assert_schema_eq_record(guest_form_schema, guest_form_orm)


@pytest.mark.usefixtures('guest_forms')
async def test_get_form_by_guest_id__not_found():
    """Validate retrieve guest form by guest_id if not exists."""
    guest_form_repository = GuestFormRepository()

    with pytest.raises(ObjectNotFoundException) as exc_info:
        await guest_form_repository.get_by_guest_id(guest_id=0)

    assert repr(exc_info.value) == 'Object Not Found: guest form guest_id=0'


async def test_create_guest_form(guests: list[Guest]):
    """Validate create guest form."""
    guest_form_repository = GuestFormRepository()

    guest_orm = guests[0]
    guest_form_schema = GuestFormSchema(
        guest_id=guest_orm.guest_id,
        stage=GuestFormStageEnum.COMPLETED,
        additional_info='Allergic to fruits.',
    )

    await guest_form_repository.create(guest_form=guest_form_schema)

    guest_form_orm = await GuestForm.get(guest_id=guest_orm.guest_id)
    _assert_schema_eq_record(guest_form_schema, guest_form_orm)


async def test_create_guest_form__already_exists(guest_forms: list[GuestForm]):
    """Validate create guest form if exists."""
    guest_form_repository = GuestFormRepository()

    guest_form_orm = guest_forms[0]
    guest_form_updated_at = guest_form_orm.updated_at

    new_guest_form_schema = GuestFormSchema(
        guest_id=guest_form_orm.guest_id,
        stage=GuestFormStageEnum.DECLINED,
        additional_info=None,
    )

    with pytest.raises(IntegrityError):
        await guest_form_repository.create(guest_form=new_guest_form_schema)

    guest_form_orm = await GuestForm.get(guest_id=guest_form_orm.guest_id)
    assert guest_form_orm.updated_at == guest_form_updated_at
    assert guest_form_orm.created_at <= guest_form_updated_at


async def test_partial_update_guest_form(guest_forms: list[GuestForm]):
    """Validate update of guest forms."""
    guest_form_repository = GuestFormRepository()

    guest_form_orm = guest_forms[0]
    patch_guest_form_schema = GuestFormSchema(
        guest_id=guest_form_orm.guest_id,
        stage=GuestFormStageEnum.FILLING_ADDITIONAL_INFO,
    )

    await guest_form_repository.partial_update(guest_form=patch_guest_form_schema)

    guest_form_orm = await GuestForm.get(guest_id=guest_form_orm.guest_id)
    _assert_schema_eq_record(patch_guest_form_schema, guest_form_orm)

    patch_guest_form_schema = GuestFormSchema(
        guest_id=guest_form_orm.guest_id,
        stage=GuestFormStageEnum.COMPLETED,
        additional_info='Not really.',
    )

    await guest_form_repository.partial_update(guest_form=patch_guest_form_schema)

    guest_form_orm = await GuestForm.get(guest_id=guest_form_orm.guest_id)
    _assert_schema_eq_record(patch_guest_form_schema, guest_form_orm)


async def test_partial_update_guest_form__not_found():
    """Validate update of guest forms if not exists."""
    guest_form_repository = GuestFormRepository()

    guest_form_schema = GuestFormSchema(
        guest_id=0,
        stage=GuestFormStageEnum.COMPLETED,
        additional_info=None,
    )

    with pytest.raises(ObjectNotFoundException) as exc_info:
        await guest_form_repository.partial_update(guest_form=guest_form_schema)

    assert repr(exc_info.value) == 'Object Not Found: guest form guest_id=0'


def _assert_schema_eq_record(schema: GuestFormSchema, orm_record: GuestForm) -> None:
    """Assert schema contains data of needed record."""
    assert schema.guest_id == orm_record.guest_id
    assert schema.stage == orm_record.stage
    assert schema.additional_info == orm_record.additional_info
