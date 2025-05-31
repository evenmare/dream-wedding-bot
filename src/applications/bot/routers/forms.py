"""Module contains form stage routers."""

from functools import partial

from dependency_injector.wiring import Provide, inject
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    CallbackQuery,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from tortoise.transactions import atomic

from applications.bot.context import request_guest, request_guest_form
from applications.bot.services import ReplyMarkupFactory, SendMessageService
from containers import Container
from entities.enums.forms import GuestFormStageEnum
from entities.schemas.callbacks import CommandSchema
from exceptions.repositories import ObjectNotFoundException
from repositories.database.invitations import InvitationRequestRepository
from typings.services import CoordinatesTuple
from use_cases.messages_handlers.requests.callback_queries import IdentifyCallbackQueryUseCase
from use_cases.messages_handlers.requests.forms.additional_info_callback import HandleAdditionalInfoCallbackUseCase
from use_cases.messages_handlers.requests.forms.address_specification_callback import (
    HandleAddressSpecificationCallbackUseCase,
)
from use_cases.messages_handlers.requests.forms.address_input_callback import HandleAddressInputCallbackUseCase
from use_cases.messages_handlers.requests.forms.awaiting_answer_callback import HandleAwaitingAnswerCallbackUseCase
from use_cases.messages_handlers.requests.forms.geotag_validation_callback import HandleGeotagValidationCallbackUseCase
from use_cases.messages_handlers.requests.forms.invitation_neediness_callback import (
    HandleInvitationNeedinessCallbackUseCase,
)
from use_cases.messages_handlers.responses.commands import GetResponseMessageByCommandUseCase
from use_cases.messages_handlers.responses.forms import GetResponseMessageByFormStageUseCase


# TODO: refactoring
@atomic()
@inject
async def handle_form_stage_callback(
    callback_or_message: CallbackQuery | Message,
    bot: AsyncTeleBot = Provide[Container.bot],
    # Identify command
    identify_callback_use_case: IdentifyCallbackQueryUseCase = Provide[Container.identify_callback_query_use_case],
    # Handle Use Cases
    handle_awaiting_answer_callback_use_case: HandleAwaitingAnswerCallbackUseCase = Provide[
        Container.handle_awaiting_answer_callback_use_case
    ],
    handle_invitation_neediness_callback_use_case: HandleInvitationNeedinessCallbackUseCase = Provide[
        Container.handle_invitation_neediness_callback_use_case
    ],
    handle_address_input_use_case: HandleAddressInputCallbackUseCase = Provide[Container.handle_address_input_use_case],
    handle_geotag_validation_callback_use_case: HandleGeotagValidationCallbackUseCase = Provide[
        Container.handle_geotag_validation_callback_use_case
    ],
    handle_address_specification_callback_use_case: HandleAddressSpecificationCallbackUseCase = Provide[
        Container.handle_address_specification_callback_use_case
    ],
    handle_additional_info_callback_use_case: HandleAdditionalInfoCallbackUseCase = Provide[
        Container.handle_additional_info_callback_use_case
    ],
    # Get message data Use Cases
    get_response_use_case: GetResponseMessageByFormStageUseCase = Provide[Container.response_by_form_stage_use_case],
    # Send message services
    reply_markup_factory: ReplyMarkupFactory = Provide[Container.reply_markup_factory],
    send_message_service: SendMessageService = Provide[Container.send_message_service],
):
    if isinstance(callback_or_message, CallbackQuery):
        callback = callback_or_message
        message = callback_or_message.message
    else:
        callback = None
        message = callback_or_message

    guest = request_guest.get()
    guest_form = request_guest_form.get()

    match guest_form.stage:
        case GuestFormStageEnum.AWAITING_ANSWER if callback:
            command: CommandSchema[str] = await identify_callback_use_case(
                guest=guest,
                code=callback.data,
            )
            handle_callback_use_case_instance = handle_awaiting_answer_callback_use_case
            handle_callback_use_case = partial(
                handle_callback_use_case_instance,
                callback_command=command,
            )
        case GuestFormStageEnum.INVITATION_NEEDINESS_ASKED if callback:
            command: CommandSchema[str] = await identify_callback_use_case(
                guest=guest,
                code=callback.data,
            )
            handle_callback_use_case_instance = handle_invitation_neediness_callback_use_case
            handle_callback_use_case = partial(
                handle_callback_use_case_instance,
                callback_command=command,
            )
        case GuestFormStageEnum.INVITATION_ADDRESS_INPUT | GuestFormStageEnum.INVITATION_ADDRESS_TEXT_INPUT:
            location = (
                CoordinatesTuple(
                    latitude=message.location.latitude,
                    longitude=message.location.longitude,
                )
                if message.location
                else None
            )
            handle_callback_use_case_instance = handle_address_input_use_case
            handle_callback_use_case = partial(
                handle_callback_use_case_instance,
                location=location,
                text=message.text,
            )
        case GuestFormStageEnum.INVITATION_GEOTAG_VALIDATION if callback:
            command: CommandSchema[str] = await identify_callback_use_case(
                guest=guest,
                code=callback.data,
            )
            handle_callback_use_case_instance = handle_geotag_validation_callback_use_case
            handle_callback_use_case = partial(
                handle_callback_use_case_instance,
                callback_command=command,
            )
        case GuestFormStageEnum.INVITATION_INFO_SPECIFICATION:
            handle_callback_use_case_instance = handle_address_specification_callback_use_case
            handle_callback_use_case = partial(
                handle_callback_use_case_instance,
                address_specification=message.text,
            )
        case GuestFormStageEnum.FILLING_ADDITIONAL_INFO:
            handle_callback_use_case_instance = handle_additional_info_callback_use_case
            handle_callback_use_case = partial(
                handle_callback_use_case_instance,
                additional_info=message.text,
            )
        case _:
            raise NotImplementedError('unknown command.')  # TODO

    guest_form, invitation_request = await handle_callback_use_case(guest_form=guest_form)
    response_message_schema = await get_response_use_case(
        guest=guest,
        guest_form=guest_form,
        invitation_request=invitation_request,
    )

    match guest_form.stage:
        case (
            GuestFormStageEnum.AWAITING_ANSWER
            | GuestFormStageEnum.DECLINED
            | GuestFormStageEnum.INVITATION_NEEDINESS_ASKED
            | GuestFormStageEnum.INVITATION_GEOTAG_VALIDATION
            | GuestFormStageEnum.INVITATION_INFO_SPECIFICATION
            | GuestFormStageEnum.FILLING_ADDITIONAL_INFO
            | GuestFormStageEnum.INVITATION_ADDRESS_TEXT_INPUT
            | GuestFormStageEnum.COMPLETED
        ):
            reply_markup = reply_markup_factory.make_inline_keyboard(
                keyboard_buttons=response_message_schema.keyboard_buttons,
            )
        case GuestFormStageEnum.INVITATION_ADDRESS_INPUT:
            reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)

            if not response_message_schema.keyboard_buttons or len(response_message_schema.keyboard_buttons) > 1:
                raise ValueError('keyboard buttons')  # TODO

            reply_markup.add(
                KeyboardButton(
                    text=response_message_schema.keyboard_buttons[0].text,
                    request_location=True,
                )
            )

    with send_message_service(bot_instance=bot) as message_service:
        await message_service.reply(
            message=message,
            text=response_message_schema.text,
            image_url=response_message_schema.image_url,
            reply_markup=reply_markup,
        )

        await message_service.clear_inline_markup(message=message)

        if handle_callback_use_case_instance.should_delete_reply_keyboard:
            await message_service.clear_reply_markup(message=message)


@inject
async def process_form_stage_message(
    message: Message,
    bot: AsyncTeleBot = Provide[Container.bot],
    invitation_request_repository: InvitationRequestRepository = Provide[Container.invitation_request_repository],
    get_response_use_case: GetResponseMessageByFormStageUseCase = Provide[Container.response_by_form_stage_use_case],
    reply_markup_factory: ReplyMarkupFactory = Provide[Container.reply_markup_factory],
    send_message_service: SendMessageService = Provide[Container.send_message_service],
):
    """Process form stage message."""
    guest = request_guest.get()
    guest_form = request_guest_form.get()

    try:
        invitation_request = await invitation_request_repository.get_by_guest_id(guest_id=guest.guest_id)
    except ObjectNotFoundException:
        invitation_request = None

    response_message_schema = await get_response_use_case(
        guest=guest,
        guest_form=guest_form,
        invitation_request=invitation_request,
    )
    reply_markup = reply_markup_factory.make_inline_keyboard(keyboard_buttons=response_message_schema.keyboard_buttons)

    with send_message_service(bot_instance=bot) as message_service:
        return await message_service.reply(
            message=message,
            text=response_message_schema.text,
            image_url=response_message_schema.image_url,
            reply_markup=reply_markup,
        )
