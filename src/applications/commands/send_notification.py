"""Module implements logic for message send."""

from dependency_injector.wiring import inject, Provide

from applications.commands.base import BaseCommand
from containers import Container
from infrastructures.databases import init_db
from repositories.database.guests import GuestRepository
from use_cases.send_notifications import SendNotificationsUseCase


class SendNotificationCommand(BaseCommand):
    """Class implements logic for notification send command."""

    command_name = 'send-notification'

    @inject
    async def __call__(
        self,
        guest_repository: GuestRepository = Provide[Container.guest_repository],
        send_notifications_use_case: SendNotificationsUseCase = Provide[Container.send_notifications_use_case],
    ):
        """Runs a command

        :param guest_repository: Guest repository.
        :param send_notifications_use_case: Send notifications use case.
        """
        await init_db()

        guests_ids = {guest.guest_id async for guest in guest_repository.filter_all()}
        await send_notifications_use_case(
            guests_ids=frozenset(guests_ids),
            limit_on_guest=1,
        )
