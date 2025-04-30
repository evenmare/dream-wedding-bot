"""Module contains a repository for guests forms."""

from entities.database.forms import GuestForm
from entities.schemas.forms import GuestFormSchema
from repositories.database.base import BaseDatabaseRepository

__all__ = ('GuestFormRepository',)


class GuestFormRepository(BaseDatabaseRepository[GuestForm, GuestFormSchema]):
    """Class implements repository for guests entity operations."""

    schema = GuestFormSchema
    _model = GuestForm

    async def filter_by_guest_id(self, guest_id: int) -> GuestFormSchema:
        """Filter form by guest id.

        :param guest_id: Guest identity.
        :return: Guest schema.
        """
        guest_form_orm = await self._model.filter(guest_id=guest_id)
        return self._serialize_model(guest_form_orm)
