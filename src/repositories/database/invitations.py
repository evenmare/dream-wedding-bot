"""Module contains repositories for invitations entities."""

from tortoise.exceptions import DoesNotExist, IntegrityError as OrmIntegrityError

from entities.database.invitations import InvitationRequest
from entities.schemas.invitations import InvitationRequestSchema
from exceptions.repositories import IntegrityError, ObjectNotFoundException
from repositories.database.base import BaseDatabaseRepository

__all__ = ('InvitationRequestRepository',)


class InvitationRequestRepository(
    BaseDatabaseRepository[InvitationRequest, InvitationRequestSchema]
):
    """Class implements a repository for InvitationRequest entity."""

    schema = InvitationRequestSchema
    _model = InvitationRequest

    async def get_by_guest_id(self, guest_id: int) -> InvitationRequestSchema:
        """Get invitation request by guest_id.

        :param guest_id: Guest identity.
        :raises ObjectNotFoundException: If does not exist.
        :return: Invitation request schema.
        """
        try:
            guest_orm = await self._model.get(guest_id=guest_id)
        except DoesNotExist as exc:
            raise ObjectNotFoundException(
                f'invitation request guest_id={guest_id}',
            ) from exc

        return guest_orm

    async def create(self, invitation_request: InvitationRequestSchema) -> None:
        """Creates a new invitation request record.

        :param invitation_request: Invitation request schema.
        :raises IntegrityError: If invitation request already exists.
        """
        item_repr = invitation_request.model_dump(exclude_unset=True)

        try:
            await self._model.create(**item_repr)
        except OrmIntegrityError as exc:
            raise IntegrityError(details=str(exc))

    async def partial_update(self, invitation_request: InvitationRequestSchema) -> None:
        """Updates an existing invitation request record.

        :param invitation_request: Invitation request schema.
        :raises ObjectNotFoundException: If does not exist.
        """
        guest_id = invitation_request.guest_id
        item_repr = invitation_request.model_dump(
            exclude={'guest_id'},
            exclude_unset=True,
        )

        base_query = self._model.filter(guest_id=guest_id)

        if not await base_query.exists():
            raise ObjectNotFoundException(f'invitation request guest_id={guest_id}')

        await base_query.update(**item_repr)
