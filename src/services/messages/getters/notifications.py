"""Module contains class for notification message data getter."""

from exceptions.repositories import ObjectNotFoundException
from exceptions.services import CallbackMessageNotFoundException
from services.messages.getters.base import BaseMessageDataGetter
from typings.services import MessageFactoryDataTuple


class NotificationMessageDataGetter(BaseMessageDataGetter[MessageFactoryDataTuple]):
    """Notification response data getter service."""

    async def __call__(
        self,
        *,
        notification_id: int,
    ) -> MessageFactoryDataTuple[None]:
        """Get notification response base data.

        :param notification_id: Notification identity.
        :return: Message factory data.
        """
        try:
            callback_message = await self._callback_message_repository.get_by_notification_id(
                notification_id=notification_id
            )
        except ObjectNotFoundException as exc:
            raise CallbackMessageNotFoundException from exc

        return MessageFactoryDataTuple(message_ref=callback_message, commands=[])
