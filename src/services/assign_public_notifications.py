"""Module contains service for assign notifications for guest."""

from repositories.database.notifications import NotificationRepository


class AssignPublicNotificationsService:
    """Service implements logic for assign notifications for guest."""

    def __init__(self, notification_repository: NotificationRepository):
        """Class constructor.

        :param notification_repository: Repository for notifications.
        """
        self.__notification_repository = notification_repository

    async def __call__(self, guests_ids: set[int]) -> None:
        """Assign public notifications for guests.

        :param guests_ids: Identities of guests.
        """
        public_notifications_ids = {
            notification.notification_id async for notification in self.__notification_repository.filter_public()
        }

        guest_id_notification_id_pairs: list[tuple[int, int]] = []

        for guest_id in guests_ids:
            guest_notifications_ids = {
                notification.notification_id
                async for notification in self.__notification_repository.filter_available(guest_id=guest_id)
            }

            notifications_ids_to_assign = public_notifications_ids - guest_notifications_ids
            guest_id_notification_id_pairs.extend(
                [(guest_id, notification_id) for notification_id in notifications_ids_to_assign]
            )

        await self.__notification_repository.assign_to_guest(
            guest_notification_pairs=frozenset(guest_id_notification_id_pairs)
        )
