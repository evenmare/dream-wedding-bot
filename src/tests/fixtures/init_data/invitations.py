"""Module contains test data for InvitationRequest entity."""

from collections.abc import AsyncGenerator

import pytest

from entities.database.guests import Guest
from entities.database.invitations import InvitationRequest


def _generate_invitation_request(guests: list[Guest]) -> list[InvitationRequest]:
    """Generates list of invitation requests."""
    return [
        InvitationRequest(
            address='Moscow',
            address_specification=None,
            guest=guests[0],
        ),
        InvitationRequest(
            address='Saint Petersburg, Nevsky strict, 3',
            address_specification='ft 1',
            guest=guests[1],
        ),
    ]


@pytest.fixture(scope='function')
async def invitation_requests(
    db: AsyncGenerator[None, None],
    guests: list[Guest],
):
    """Creates invitation requests list."""
    invitation_requests_orm = _generate_invitation_request(guests=guests)
    await InvitationRequest.bulk_create(invitation_requests_orm)
    return list(await InvitationRequest.all())
