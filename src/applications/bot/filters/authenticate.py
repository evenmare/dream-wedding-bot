"""Module contains Telebot filter for authenication check."""

from typing import assert_never
from dependency_injector.wiring import inject, Provide

from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import Message, CallbackQuery

from containers import Container
from applications.bot.context import request_guest
from entities.schemas.telegram import TelegramUserSchema
from exceptions.use_cases import NotAuthenticatedException
from use_cases.authenticate import AuthenticationUseCase


class IsAuthenticatedFilter(SimpleCustomFilter):
    """Check if user is authenticated as a guest."""

    key = 'is_authenticated'

    @staticmethod
    @inject
    async def check(
        message: Message | CallbackQuery,
        use_case: AuthenticationUseCase = Provide[Container.authentication_use_case],
    ) -> bool:
        """Check if user is authenticated as a guest.

        :param message: Telebot Message object.
        """
        match message:
            case Message():
                chat_id = message.chat.id
                username = message.chat.username
            case CallbackQuery():
                chat_id = message.message.chat.id
                username = message.message.chat.username
            case _:
                assert_never()

        telegram_user_schema = TelegramUserSchema(
            user_id=chat_id,
            username=username,
        )

        try:
            guest_schema = await use_case(telegram_user_schema)
        except NotAuthenticatedException:
            return False

        request_guest.set(guest_schema)
        return bool(guest_schema)
