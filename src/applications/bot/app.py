"""Module contains bot app implementation."""

from dependency_injector.wiring import inject, Provide

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from applications.bot.filters.authenticate import IsAuthenticatedFilter
from applications.bot.filters.forms import FormStageFilter
from applications.bot.routers.commands import handle_command_callback, get_message_form_filled
from applications.bot.routers.forms import handle_form_stage_callback, process_form_stage_message
from applications.bot.routers.initial_commands import register, request_contact
from applications.bot.services import SendMessageService
from containers import Container
from entities.enums.forms import GuestFormStageEnum


@inject
async def check_health(
    message: Message,
    bot: AsyncTeleBot = Provide[Container.bot],
    send_message_service: SendMessageService = Provide[Container.send_message_service],
):
    """Check if bot is alive."""
    with send_message_service(bot_instance=bot) as message_service:
        await message_service.reply(message=message, text='&#9989')


@inject
async def run_bot(bot: AsyncTeleBot = Provide[Container.bot]) -> None:
    """Run bot.

    :param config: Config for bot.
    """
    bot.add_custom_filter(IsAuthenticatedFilter())
    bot.add_custom_filter(FormStageFilter())

    bot.message_handler(commands=('is_alive',))(check_health)

    # Registration
    bot.message_handler(
        content_types=('contact',),
        is_authenticated=False,
    )(register)
    bot.message_handler(commands=('start',), is_authenticated=False)(request_contact)
    bot.message_handler(is_authenticated=False)(request_contact)

    # Form stages
    bot.message_handler(
        commands=('start', 'resend',),
        is_authenticated=True,
        form_stage=(
            GuestFormStageEnum.AWAITING_ANSWER,
            GuestFormStageEnum.INVITATION_NEEDINESS_ASKED,
            GuestFormStageEnum.INVITATION_GEOTAG_VALIDATION,
        ),
    )(process_form_stage_message)
    bot.callback_query_handler(
        func=lambda callback: True,
        is_authenticated=True,
        form_stage=(
            GuestFormStageEnum.AWAITING_ANSWER,
            GuestFormStageEnum.INVITATION_NEEDINESS_ASKED,
            GuestFormStageEnum.INVITATION_GEOTAG_VALIDATION,
        ),
    )(handle_form_stage_callback)
    bot.message_handler(
        content_types=('location', 'text'),
        is_authenticated=True,
        form_stage=(
            GuestFormStageEnum.INVITATION_ADDRESS_INPUT,
            GuestFormStageEnum.INVITATION_ADDRESS_TEXT_INPUT,
        ),
    )(handle_form_stage_callback)
    bot.message_handler(
        is_authenticated=True,
        form_stage=(
            GuestFormStageEnum.INVITATION_INFO_SPECIFICATION,
            GuestFormStageEnum.FILLING_ADDITIONAL_INFO,
        )
    )(handle_form_stage_callback)

    # Commands stage
    bot.message_handler(
        commands=('start', 'resend',),
        is_authenticated=True,
        form_stage=(GuestFormStageEnum.COMPLETED,),
    )(get_message_form_filled)
    bot.callback_query_handler(
        func=lambda callback: True,
        is_authenticated=True,
        form_stage=(GuestFormStageEnum.COMPLETED,),
    )(handle_command_callback)

    await bot.infinity_polling()
