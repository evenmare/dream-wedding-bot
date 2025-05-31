"""Module contains commands routes implementations."""

from dependency_injector.wiring import Provide, inject
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from applications.bot.context import request_guest, request_guest_form
from applications.bot.services import ReplyMarkupFactory, SendMessageService
from containers import Container
from entities.schemas.callbacks import MessageSchema
from use_cases.messages_handlers.requests.callback_queries import IdentifyCallbackQueryUseCase
from use_cases.messages_handlers.responses.commands import GetResponseMessageByCommandUseCase


@inject
async def handle_command_callback(
    callback: CallbackQuery,
    bot: AsyncTeleBot = Provide[Container.bot],
    identify_callback_use_case: IdentifyCallbackQueryUseCase = Provide[Container.identify_callback_query_use_case],
    get_message_use_case: GetResponseMessageByCommandUseCase = Provide[Container.response_by_command_use_case],
    reply_markup_factory: ReplyMarkupFactory = Provide[Container.reply_markup_factory],
    send_message_service: SendMessageService = Provide[Container.send_message_service],
):
    """Handle message while form filling."""
    guest = request_guest.get()

    command = await identify_callback_use_case(guest=guest, code=callback.data)
    response_message_schema: MessageSchema = await get_message_use_case(
        command=command,
        guest=request_guest.get(),
        guest_form=request_guest_form.get(),
    )

    reply_markup = reply_markup_factory.make_inline_keyboard(keyboard_buttons=response_message_schema.keyboard_buttons)
    with send_message_service(bot_instance=bot) as message_service:
        await message_service.update_on_callback(
            callback,
            text=response_message_schema.text,
            image_url=response_message_schema.image_url,
            reply_markup=reply_markup,
        )


@inject
async def get_message_form_filled(
    message: Message,
    bot: AsyncTeleBot = Provide[Container.bot],
    identify_callback_use_case: IdentifyCallbackQueryUseCase = Provide[Container.identify_callback_query_use_case],
    get_response_use_case: GetResponseMessageByCommandUseCase = Provide[Container.response_by_command_use_case],
    reply_markup_factory: ReplyMarkupFactory = Provide[Container.reply_markup_factory],
    send_message_service: SendMessageService = Provide[Container.send_message_service],
):
    """Get default message after form filled."""
    guest = request_guest.get()
    guest_form = request_guest_form.get()

    command = await identify_callback_use_case(guest=guest, strict=False)
    response_message_schema = await get_response_use_case(
        command=command,
        guest=guest,
        guest_form=guest_form,
    )

    reply_markup = reply_markup_factory.make_inline_keyboard(keyboard_buttons=response_message_schema.keyboard_buttons)
    with send_message_service(bot_instance=bot) as message_service:
        await message_service.reply(
            message=message,
            text=response_message_schema.text,
            image_url=response_message_schema.image_url,
            reply_markup=reply_markup,
        )