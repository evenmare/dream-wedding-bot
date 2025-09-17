"""Module contains notifications access repository."""

from typing import AsyncGenerator

from entities.database.notifications import PersonalNotification, Notification
from entities.schemas.notifications import NotificationSchema
from repositories.database.base import BaseManyToManyRepository


class NotificationRepository(BaseManyToManyRepository[Notification, PersonalNotification, NotificationSchema]):
    """Class implements notification access repository."""

    schema = NotificationSchema
    _model = Notification
    _m2m_model = PersonalNotification

    async def filter_public(self) -> AsyncGenerator[NotificationSchema, None]:
        """Method returns generator of all public notifications.

        :return: Generator of public notifications.
        """
        query = self._model.filter(is_personal=False).order_by('created_at')

        notifications_iterator = aiter(query)

        async for notification_orm in notifications_iterator:
            yield self._serialize_model(notification_orm)

    async def filter_available(
        self,
        guest_id: int,
        *,
        limit: int | None = None,
    ) -> AsyncGenerator[NotificationSchema, None]:
        """Method returns all notifications for sending.

        :param guest_id: Guest identificator.
        :return: Async generator of notifications.
        """
        query = self._model.filter(
            guests__guest_id=guest_id,
            personal_notification__is_sent=False,
        ).order_by('created_at')

        if limit:
            query = query.limit(limit)

        notifications_iterator = aiter(query)

        async for notification_orm in notifications_iterator:
            yield self._serialize_model(notification_orm)

    async def assign_to_guest[_GuestId = int, _NotificationId = int](
        self,
        guest_notification_pairs: frozenset[tuple[_GuestId, _NotificationId]],
    ) -> None:
        """Method makes notification available for guests.

        :param guest_notification_pairs: Guest-Notification identificators pair.
        """
        personal_notifications_orm: list[PersonalNotification] = [
            PersonalNotification(
                guest_id=guest_id,
                notification_id=notification_id,
            )
            for guest_id, notification_id in guest_notification_pairs
        ]

        await self._m2m_model.bulk_create(personal_notifications_orm)

    async def mark_as_sent(
        self,
        guest_id: int,
        notifications_ids: frozenset[int],
    ) -> None:
        """Method marks notifications as sent.

        :param notifications_ids: Set of Notification identities.
        """
        await self._m2m_model.filter(
            guest_id=guest_id,
            notification_id__in=notifications_ids,
        ).update(is_sent=True)
