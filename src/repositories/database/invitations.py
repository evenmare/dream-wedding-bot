"""Module contains repositories for invitations entities."""

from entities.database.invitations import InvitationRequest
from entities.schemas.invitations import InvitationRequestSchema
from repositories.database.base import BaseDatabaseRepository

__all__ = ('InvitationRequestRepository',)


class InvitationRequestRepository(
    BaseDatabaseRepository[InvitationRequest, InvitationRequestSchema]
):
    """Class implements a repository for InvitationRequest entity."""

    schema = InvitationRequestSchema
    _model = InvitationRequest

    async def create(self, invitation_request: InvitationRequestSchema) -> None:
        """Creates a new invitation request record.

        :param invitation_request: Invitation request schema.
        """
        item_repr = invitation_request.model_dump(exclude_unset=True)
        await self._model.create(**item_repr)

    async def partial_update(self, invitation_request: InvitationRequestSchema) -> None:
        """Updates an existing invitation request record."""
        guest_id = invitation_request.guest_id
        item_repr = invitation_request.model_dump(
            exclude={'guest_id'},
            exclude_unset=True,
        )
        await self._model.filter(guest_id=guest_id).update(**item_repr)
