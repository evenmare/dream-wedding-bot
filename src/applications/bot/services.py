"""Module contains services for Telegram Bot."""

import contextlib
from typing import Self
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_helper import ApiTelegramException
from telebot.types import (
    Message,
    InaccessibleMessage,
    CallbackQuery,
    InputMediaPhoto,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from configs.applications import MessageConfig
from entities.schemas.commands import CommandSchema


class ReplyMarkupFactory:
    """Factory of reply markup."""

    def __init__(self, message_config: MessageConfig) -> None:
        """Class constructor.

        :param message_config: Config for bot messages.
        """
        self._message_config = message_config

    def make_inline_keyboard(self, keyboard_buttons: list[CommandSchema[str]]) -> InlineKeyboardMarkup | None:
        """Make inline keyboard.

        :param keyboard_buttons: List of available commands.
        :return: InlineKeyboardMarkup if commands provided.
        """
        reply_markup = None
        if keyboard_buttons:
            reply_markup = InlineKeyboardMarkup(row_width=self._message_config.INLINE_KEYBOARD_ROW_WIDTH)
            reply_markup.add(
                *[
                    InlineKeyboardButton(
                        text=keyboard_button.text,
                        callback_data=keyboard_button.code,
                    )
                    for keyboard_button in keyboard_buttons
                ]
            )

        return reply_markup


class SendMessageService:
    """Service implements sending message logic."""

    __bot: AsyncTeleBot

    async def send(
        self,
        chat_id: int,
        *,
        text: str,
        image_url: str | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | None = None,
    ) -> Message:
        """Send message.

        :param text: Test of message.
        :param image_url: Image url if provided, defaults to None
        :param reply_markup: Reply markup if provided, defaults to None
        :return: Sent message.
        """
        if image_url:
            return await self.__bot.send_photo(
                chat_id=chat_id,
                photo=image_url,
                caption=text,
                reply_markup=reply_markup,
                parse_mode='html',
            )

        return await self.__bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode='html',
        )

    async def reply(
        self,
        message: Message,
        *,
        text: str,
        image_url: str | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | None = None,
    ) -> Message:
        """Reply to message.

        :param message: Message to reply.
        :param text: Text of message.
        :param image_url: Image url if provided, defaults to None
        :param reply_markup: Reply markup if provided, defaults to None
        """
        if image_url:
            return await self.__bot.send_photo(
                chat_id=message.chat.id,
                photo=image_url,
                caption=text,
                reply_markup=reply_markup,
                reply_to_message_id=message.id,
                parse_mode='html',
            )

        return await self.__bot.reply_to(
            message=message,
            text=text,
            reply_markup=reply_markup,
            parse_mode='html',
        )

    async def clear_reply_markup(self, message: Message | InaccessibleMessage) -> None:
        """Send message to remove reply markup and instantly delete it.

        :param message: Message.
        """
        reply_markup = ReplyKeyboardRemove()
        remove_keyboard_message: Message = await self.reply(
            message=message,
            text='%processing%',
            reply_markup=reply_markup,
        )

        await self.__bot.delete_message(
            chat_id=remove_keyboard_message.chat.id,
            message_id=remove_keyboard_message.message_id,
        )

    async def clear_inline_markup(
        self,
        message: Message | InaccessibleMessage,
    ) -> Message | bool | None:
        """Update message and clear existing markup.

        :param message: Message.
        """
        with contextlib.suppress(ApiTelegramException):
            return await self.__bot.edit_message_reply_markup(
                reply_markup=None,
                chat_id=message.chat.id,
                message_id=message.message_id,
            )

    async def update_on_callback(
        self,
        callback: CallbackQuery,
        *,
        text: str,
        image_url: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Update message.

        If message can not be updated (due to type of message difference),
        it will:
            - Try to delete old message and send a new one.
            - If delete can not be performed, it will update message to set
                reply markup to None.

        :param message: Message to reply.
        :param text: Text of message.
        :param image_url: Image url if provided, defaults to None
        :param reply_markup: Reply markup if provided, defaults to None
        """
        message = callback.message

        if message.photo:
            if image_url:
                try:
                    return await self.__bot.edit_message_media(
                        media=InputMediaPhoto(
                            media=image_url,
                            caption=text,
                            parse_mode='html',
                        ),
                        reply_markup=reply_markup,
                        chat_id=message.chat.id,
                        message_id=message.message_id,
                    )
                except ApiTelegramException:
                    return await self.__bot.answer_callback_query(callback_query_id=callback.id)

            try:
                await self.__bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except ApiTelegramException:
                await self.clear_inline_markup(message)

            return await self.__bot.send_message(
                text=text,
                reply_markup=reply_markup,
                chat_id=message.chat.id,
                parse_mode='html',
            )

        if image_url:
            try:
                await self.__bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except ApiTelegramException:
                await self.clear_inline_markup(message)

            return await self.__bot.send_photo(
                photo=image_url,
                caption=text,
                reply_markup=reply_markup,
                reply_to_message_id=message.id,
                allow_sending_without_reply=True,
                chat_id=message.chat.id,
                parse_mode='html',
            )

        with contextlib.suppress(ApiTelegramException):
            return await self.__bot.edit_message_text(
                text=text,
                reply_markup=reply_markup,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode='html',
            )

        return await self.__bot.answer_callback_query(callback_query_id=callback.id)

    def __enter__(self):
        """Open context manager."""
        return self

    def __call__(self, bot_instance: AsyncTeleBot) -> Self:
        """Set bot instance to class.

        :param bot_instance: Bot instance.
        :return: Self.
        """
        self.__bot = bot_instance
        return self

    def __exit__(
        self,
        *_,
        **__,
    ) -> bool | None:
        """Exit from context manager."""
        self.__bot = None
