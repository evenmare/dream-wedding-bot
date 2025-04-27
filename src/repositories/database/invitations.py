"""Module contains repositories for invitations entities."""

from entities.database.invitations import InvitationRequest
from entities.schemas.invitations import InvitationRequestSchema
from repositories.database.base import BaseDatabaseRepository

__all__ = ('InvitationsRequestsRepository',)


class InvitationsRequestsRepository(
    BaseDatabaseRepository[InvitationRequest, InvitationRequestSchema]
):
    """Class implements a repository for InvitationRequest entity."""

    schema = InvitationRequestSchema
    __model = InvitationRequest

    async def get_by_guest_id(self, guest_id: int) -> InvitationRequestSchema | None:
        """Get an invitation request by guest id.

        :param guest_id: Guest record id.
        :return: Schema for invitation request record for guest if exists, None otherwise.
        """
        request_orm = await self.__model.get_or_none(guest_id=guest_id)

        if not request_orm:
            return None

        return self._serialize_model(request_orm)

    async def create(self, invitation_request: InvitationRequestSchema) -> None:
        """Creates a new invitation request record.

        :param invitation_request: Invitation request schema.
        """
        item_repr = invitation_request.model_dump(exclude_unset=True)
        await self.__model.create(**item_repr)

    async def partial_update(self, invitation_request: InvitationRequestSchema) -> None:
        """Updates an existing invitation request record."""
        guest_id = invitation_request.guest_id
        item_repr = invitation_request.model_dump(
            exclude={'guest_id'},
            exclude_unset=True,
        )
        await self.__model.filter(guest_id=guest_id).update(**item_repr)
