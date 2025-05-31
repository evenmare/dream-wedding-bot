"""Module conatins initial commands routes implementations."""

from dependency_injector.wiring import Provide, inject
from telebot.async_telebot import AsyncTeleBot
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup
from tortoise.transactions import atomic

from applications.bot.context import request_guest, request_guest_form
from applications.bot.routers.forms import process_form_stage_message
from applications.bot.services import SendMessageService
from containers import Container
from entities.enums.initial_commands import InitialCommandEnum
from entities.schemas.callbacks import MessageSchema
from entities.schemas.telegram import TelegramUserSchema
from exceptions.use_cases import NotAuthenticatedException
from use_cases.messages_handlers.responses.initial_commands import GetResponseMessageByInitialCommandUseCase
from use_cases.register import RegistrationUseCase


@atomic()
@inject
async def register(
    message: Message,
    bot: AsyncTeleBot = Provide[Container.bot],
    registration_use_case: RegistrationUseCase = Provide[Container.registration_use_case],
    get_error_message_use_case: GetResponseMessageByInitialCommandUseCase = Provide[
        Container.response_by_initial_command_use_case
    ],
    send_message_service: SendMessageService = Provide[Container.send_message_service],
):
    """Register user."""
    phone_number = message.contact.phone_number
    user_schema = TelegramUserSchema(
        user_id=message.chat.id,
        username=message.chat.username,
    )

    try:
        guest_schema, guest_form_schema = await registration_use_case(
            phone_number=phone_number,
            user_schema=user_schema,
        )
    except NotAuthenticatedException:
        initial_command = InitialCommandEnum.REGISTRATION_FAILED
        response_message_schema = await get_error_message_use_case(initial_command=initial_command)

        with send_message_service(bot_instance=bot) as message_service:
            return await message_service.reply(
                message=message,
                text=response_message_schema.text,
                image_url=response_message_schema.image_url,
            )

    with send_message_service(bot_instance=bot) as message_service:
        await message_service.clear_reply_markup(message=message)

    request_guest.set(guest_schema)
    request_guest_form.set(guest_form_schema)

    return await process_form_stage_message(message=message)


@inject
async def request_contact(
    message: Message,
    bot: AsyncTeleBot = Provide[Container.bot],
    use_case: GetResponseMessageByInitialCommandUseCase = Provide[Container.response_by_initial_command_use_case],
    send_message_service: SendMessageService = Provide[Container.send_message_service],
):
    """Start communication."""
    initial_command = InitialCommandEnum.REQUEST_CONTACT
    response_message_schema: MessageSchema = await use_case(initial_command=initial_command)

    if not response_message_schema.keyboard_buttons:
        raise ValueError('keyboard buttons')  # TODO
    if len(response_message_schema.keyboard_buttons) > 1:
        raise ValueError('keyboard buttons')  # TODO

    reply_markup = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    reply_markup.add(
        KeyboardButton(
            text=response_message_schema.keyboard_buttons[0].text,
            request_contact=True,
        )
    )

    with send_message_service(bot_instance=bot) as message_service:
        await message_service.reply(
            message=message,
            text=response_message_schema.text,
            image_url=response_message_schema.image_url,
            reply_markup=reply_markup,
        )