"""Module contains sync of personal notifications implementation."""

from dependency_injector.wiring import inject, Provide

from applications.commands.base import BaseCommand
from containers import Container
from infrastructures.databases import init_db
from repositories.database.guests import GuestRepository
from services.assign_public_notifications import AssignPublicNotificationsService


class AssignPublicNotificationsCommand(BaseCommand):
    """Class implements logic for sync available commands command."""

    command_name = 'assign-public-notifications'

    @inject
    async def __call__(
        self,
        guest_repository: GuestRepository = Provide[Container.guest_repository],
        assign_public_notifications_service: AssignPublicNotificationsService = Provide[
            Container.assign_public_notifications_service
        ],
    ) -> None:
        """Runs a command.

        :param guest_repository: Guest repository.
        :param update_available_commands_service: Update available commands service.
        """
        await init_db()

        guests_ids = {
            guest.guest_id
            async for guest in guest_repository.filter_all()
        }
        await assign_public_notifications_service(guests_ids=guests_ids)