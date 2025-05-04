"""Module contains a repository for guests forms."""

from tortoise.exceptions import DoesNotExist, IntegrityError as OrmIntegrityError

from entities.database.forms import GuestForm
from entities.schemas.forms import GuestFormSchema
from exceptions.repositories import IntegrityError, ObjectNotFoundException
from repositories.database.base import BaseDatabaseRepository

__all__ = ('GuestFormRepository',)


class GuestFormRepository(BaseDatabaseRepository[GuestForm, GuestFormSchema]):
    """Class implements repository for guests entity operations."""

    schema = GuestFormSchema
    _model = GuestForm

    async def get_by_guest_id(self, guest_id: int) -> GuestFormSchema:
        """Filter form by guest id.

        :param guest_id: Guest identity.
        :raises ObjectNotFoundException: If guest form does not exist.
        :return: Guest schema.
        """
        try:
            guest_form_orm = await self._model.get(guest_id=guest_id)
        except DoesNotExist as exc:
            raise ObjectNotFoundException(
                f'guest form guest_id={guest_id}',
            ) from exc
        return self._serialize_model(guest_form_orm)

    async def create(self, guest_form: GuestFormSchema) -> None:
        """Create guest form.

        :param guest_form: Guest form schema.
        :raises IntegrityError: If guest form already exists.
        """
        try:
            await self._model.create(**guest_form.model_dump())
        except OrmIntegrityError as exc:
            raise IntegrityError(str(exc))

    async def partial_update(self, guest_form: GuestFormSchema) -> None:
        """Update guest form.

        :param guest_form: Guest form schema.
        :raises ObjectNotFoundException: If not exists.
        """
        base_query = self._model.filter(guest_id=guest_form.guest_id)

        if not await base_query.exists():
            raise ObjectNotFoundException(f'guest form guest_id={guest_form.guest_id}')

        await base_query.update(
            **guest_form.model_dump(exclude_unset=True, exclude={'guest_id'}),
        )
