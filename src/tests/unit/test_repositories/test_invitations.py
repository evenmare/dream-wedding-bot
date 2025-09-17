"""Module contains inviration requests tests."""

import pytest

from entities.database.invitations import InvitationRequest
from entities.database.guests import Guest
from entities.schemas.invitations import InvitationRequestSchema
from exceptions.repositories import IntegrityError, ObjectNotFoundException
from repositories.database.invitations import InvitationRequestRepository

pytestmark = pytest.mark.usefixtures(
    'db',
)


async def test_get_invitation_request_by_guest_id(
    guests: list[Guest],
    invitation_requests: list[InvitationRequest],
):
    """Validate retrieve invitation request by guest_id."""
    invitation_request_repository = InvitationRequestRepository()

    invitation_request_orm = invitation_requests[0]
    invitation_request_schema = await invitation_request_repository.get_by_guest_id(
        guest_id=invitation_request_orm.guest_id,
    )

    _assert_schema_eq_record(invitation_request_orm, invitation_request_schema)


@pytest.mark.usefixtures('invitation_requests')
async def test_get_invitation_request_by_guest_id__not_found():
    """Validate retrieve invitation request by guest_id if not exists."""
    invitation_request_repository = InvitationRequestRepository()

    with pytest.raises(ObjectNotFoundException) as exc_info:
        await invitation_request_repository.get_by_guest_id(guest_id=0)

    assert repr(exc_info.value) == 'Object Not Found: invitation request guest_id=0'


async def test_create_invitation_request(guests: list[Guest]):
    """Validate create invitation request."""
    invitation_request_repository = InvitationRequestRepository()

    guest_orm = guests[0]
    invitation_request_schema = InvitationRequestSchema(
        guest_id=guest_orm.guest_id,
        address='No way',
        address_specification=None,
    )

    await invitation_request_repository.create(
        invitation_request=invitation_request_schema
    )

    invitation_request_orm = await InvitationRequest.get(guest_id=guest_orm.guest_id)
    _assert_schema_eq_record(invitation_request_schema, invitation_request_orm)


async def test_create_invitation_request__already_exists(
    invitation_requests: list[InvitationRequest],
):
    """Validate create invitation request if exists."""
    invitation_request_repository = InvitationRequestRepository()

    invitation_request_orm = invitation_requests[0]
    invitation_request_updated_at = invitation_request_orm.updated_at

    invitation_request_schema = InvitationRequestSchema(
        guest_id=invitation_request_orm.guest_id,
        address='Some to know',
    )

    with pytest.raises(IntegrityError):
        await invitation_request_repository.create(
            invitation_request=invitation_request_schema
        )

    invitation_request_orm = await InvitationRequest.get(
        guest_id=invitation_request_orm.guest_id
    )
    assert invitation_request_orm.updated_at == invitation_request_updated_at
    assert invitation_request_orm.created_at <= invitation_request_updated_at


async def test_partial_update_invitation_request(
    invitation_requests: list[InvitationRequest],
):
    """Validate update of invitation rquests."""
    invitation_request_repository = InvitationRequestRepository()

    invitation_request_orm = invitation_requests[1]
    invitation_request_schema = InvitationRequestSchema(
        guest_id=invitation_request_orm.guest_id,
        address='Moscow 2',
    )

    await invitation_request_repository.partial_update(
        invitation_request=invitation_request_schema
    )

    invitation_request_schema.address_specification = (
        invitation_request_orm.address_specification
    )

    invitation_request_orm = await InvitationRequest.get(
        guest_id=invitation_request_orm.guest_id
    )
    _assert_schema_eq_record(invitation_request_schema, invitation_request_orm)


async def test_partial_update_invitation_request__not_found():
    """Validate update of invitation requests if not exists."""
    invitation_request_repository = InvitationRequestRepository()

    invitation_request_schema = InvitationRequestSchema(
        guest_id=0,
        address=None,
    )

    with pytest.raises(ObjectNotFoundException) as exc_info:
        await invitation_request_repository.partial_update(
            invitation_request=invitation_request_schema
        )

    assert repr(exc_info.value) == 'Object Not Found: invitation request guest_id=0'


def _assert_schema_eq_record(
    schema: InvitationRequestSchema, orm_record: InvitationRequest
) -> None:
    """Assert schema contains data of needed record."""
    assert schema.guest_id == orm_record.guest_id
    assert schema.address == orm_record.address
    assert schema.address_specification == orm_record.address_specification
