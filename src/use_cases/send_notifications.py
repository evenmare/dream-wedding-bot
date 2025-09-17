"""Module contains service for notifications send."""

from telebot.async_telebot import AsyncTeleBot

from applications.bot.services import SendMessageService
from entities.schemas.callbacks import MessageSchema
from entities.schemas.telegram import TelegramUserSchema
from repositories.database.notifications import NotificationRepository
from repositories.database.telegram import TelegramUserRepository
from services.messages.factory import MessageFactoryService
from services.messages.getters.notifications import NotificationMessageDataGetter


class SendNotificationsUseCase:
    """Service implements notifications send functionality."""

    def __init__(
        self,
        telegram_user_repository: TelegramUserRepository,
        notification_repository: NotificationRepository,
        message_getter_service: NotificationMessageDataGetter,
        message_factory_service: MessageFactoryService,
        send_message_service: SendMessageService,  # TODO
        bot: AsyncTeleBot,  # TODO: it should be service
    ):
        """Class constructor.

        :param telegram_user_repository: Repository to access telegram users.
        :param notification_repository: Repository to access notifications.
        :param message_getter_service: Message data getter.
        :param message_factory_service: Message factory service.
        :param send_message_service: Send message service.
        :param bot: Bot instance.
        """
        self.__telegram_user_repository = telegram_user_repository
        self.__notification_repository = notification_repository
        self.__message_getter_service = message_getter_service
        self.__message_factory_service = message_factory_service
        self.__send_message_service = send_message_service
        self.__bot = bot

    async def __get_message_schema(self, notification_id: int) -> MessageSchema:
        """Get message schema for notification.

        :param notification_id: Notification identity.
        :return: Message schema.
        """
        factory_data = await self.__message_getter_service(notification_id=notification_id)
        return await self.__message_factory_service(message_factory_data=factory_data)

    async def __send_messages(self, user: TelegramUserSchema, messages: list[MessageSchema]) -> None:
        """Send message to user.

        :param user: Telegram user.
        :param messages: List of Message schema.
        """
        with self.__send_message_service(bot_instance=self.__bot) as service:
            for message in messages:
                await service.send(
                    chat_id=user.user_id,
                    text=message.text,
                    image_url=message.image_url,
                    reply_markup=None,
                )

    async def __call__(
        self,
        guests_ids: frozenset[int],
        limit_on_guest: int | None = None,
    ) -> None:
        """Start notifications sending.

        :param guests_ids: Guests to notify.
        :param limit_on_guest: Limit of notifications to send one-time (per guest).
        """
        message_by_notification_id_map: dict[int, MessageSchema] = {}

        async for guest_id, telegram_user in self.__telegram_user_repository.filter_by_guests_ids(
            guests_ids=guests_ids
        ):
            notifications_to_send = [
                _
                async for _ in self.__notification_repository.filter_available(
                    guest_id=guest_id,
                    limit=limit_on_guest,
                )
            ]

            messages_to_send: list[MessageSchema] = []
            for notification in notifications_to_send:
                notification_id = notification.notification_id

                if message := message_by_notification_id_map.get(notification_id):
                    messages_to_send.append(message)
                    continue

                message = await self.__get_message_schema(notification_id=notification_id)

                messages_to_send.append(message)
                message_by_notification_id_map[notification_id] = message

            await self.__send_messages(user=telegram_user, messages=messages_to_send)

            sent_notifications_ids = frozenset(notification.notification_id for notification in notifications_to_send)
            await self.__notification_repository.mark_as_sent(
                guest_id=guest_id,
                notifications_ids=sent_notifications_ids,
            )
