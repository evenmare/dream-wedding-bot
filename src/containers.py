"""Module implements containers."""

from telebot.async_telebot import AsyncTeleBot
from aiobotocore.session import get_session
from dependency_injector import containers, providers

from applications.bot.services import ReplyMarkupFactory, SendMessageService
from configs.applications import BotConfig
from configs.infrastractures import GeocoderConfig, StorageConfig
from configs.repositories import StorageRepositoryConfig
from configs.services import GetAddressByLocationServiceConfig, MessageFactoryServiceConfig
from configs.use_cases import IdentifyCallbackQueryUseCaseConfig
from infrastructures.geocoders import get_geocoder_client
from infrastructures.storages import get_s3_client
from repositories.database.callbacks import CallbackMessageRepository, CommandRepository
from repositories.database.forms import GuestFormRepository
from repositories.database.guests import GuestRepository
from repositories.database.invitations import InvitationRequestRepository
from repositories.database.telegram import TelegramUserRepository
from repositories.storages import StorageRepository
from services.messages.getters.initial_commands import InitialCommandDataGetter
from services.update_available_commands import UpdateAvailableCommandsService
from services.get_address_by_location import GetAddressByLocationService
from services.messages.factory import MessageFactoryService
from services.messages.getters.commands import CommandMessageDataGetter
from services.messages.getters.forms import FormMessageDataGetter
from use_cases.authenticate import AuthenticationUseCase
from use_cases.messages_handlers.requests.callback_queries import IdentifyCallbackQueryUseCase
from use_cases.messages_handlers.requests.forms.additional_info_callback import HandleAdditionalInfoCallbackUseCase
from use_cases.messages_handlers.requests.forms.address_specification_callback import HandleAddressSpecificationCallbackUseCase
from use_cases.messages_handlers.requests.forms.address_input_callback import HandleAddressInputCallbackUseCase
from use_cases.messages_handlers.requests.forms.awaiting_answer_callback import HandleAwaitingAnswerCallbackUseCase
from use_cases.messages_handlers.requests.forms.geotag_validation_callback import HandleGeotagValidationCallbackUseCase
from use_cases.messages_handlers.requests.forms.invitation_neediness_callback import HandleInvitationNeedinessCallbackUseCase
from use_cases.messages_handlers.responses.commands import GetResponseMessageByCommandUseCase
from use_cases.messages_handlers.responses.forms import GetResponseMessageByFormStageUseCase
from use_cases.messages_handlers.responses.initial_commands import GetResponseMessageByInitialCommandUseCase
from use_cases.register import RegistrationUseCase


class Container(containers.DeclarativeContainer):
    """Dependency injection container."""

    # Infrastracture
    storage_config = providers.Singleton(StorageConfig)
    storage_session = providers.Singleton(get_session)
    storage_client = providers.Resource(
        get_s3_client,
        session=storage_session,
        config=storage_config,
    )

    geocoder_config = providers.Singleton(GeocoderConfig)
    geocoder_client = providers.Resource(
        get_geocoder_client,
        config=geocoder_config,
    )

    # Repositories
    storage_repository_config = providers.Singleton(StorageRepositoryConfig)
    storage_repository = providers.Factory(
        StorageRepository,
        client=storage_client,
        config=storage_repository_config,
    )

    command_repository = providers.Factory(CommandRepository)
    callback_message_repository = providers.Factory(CallbackMessageRepository)
    guest_form_repository = providers.Factory(GuestFormRepository)
    guest_repository = providers.Factory(GuestRepository)
    invitation_request_repository = providers.Factory(InvitationRequestRepository)
    telegram_user_repository = providers.Factory(TelegramUserRepository)

    # Services
    get_address_by_location_service_config = providers.Singleton(GetAddressByLocationServiceConfig)
    get_address_by_location_service = providers.Factory(
        GetAddressByLocationService,
        geocoder=geocoder_client,
        config=get_address_by_location_service_config,
    )

    initial_command_data_getter = providers.Factory(
        InitialCommandDataGetter,
        callback_message_repository=callback_message_repository,
        command_repository=command_repository,
    )
    form_message_data_getter = providers.Factory(
        FormMessageDataGetter,
        callback_message_repository=callback_message_repository,
        command_repository=command_repository,
    )
    command_message_data_getter = providers.Factory(
        CommandMessageDataGetter,
        callback_message_repository=callback_message_repository,
        command_repository=command_repository,
    )

    message_factory_service_config = providers.Singleton(MessageFactoryServiceConfig)
    message_factory_service = providers.Factory(
        MessageFactoryService,
        storage_repository=storage_repository,
        config=message_factory_service_config,
    )

    update_available_commands_service = providers.Factory(
        UpdateAvailableCommandsService,
        command_repository=command_repository,
    )

    # Use Cases
    authentication_use_case = providers.Factory(
        AuthenticationUseCase,
        guest_repository=guest_repository,
        telegram_user_repository=telegram_user_repository,
    )
    registration_use_case = providers.Factory(
        RegistrationUseCase,
        guest_repository=guest_repository,
        guest_form_repository=guest_form_repository,
        telegram_user_repository=telegram_user_repository,
    )

    response_by_initial_command_use_case = providers.Factory(
        GetResponseMessageByInitialCommandUseCase,
        getter_service=initial_command_data_getter,
        factory_service=message_factory_service,
    )
    response_by_form_stage_use_case = providers.Factory(
        GetResponseMessageByFormStageUseCase,
        getter_service=form_message_data_getter,
        factory_service=message_factory_service,
    )
    response_by_command_use_case = providers.Factory(
        GetResponseMessageByCommandUseCase,
        getter_service=command_message_data_getter,
        factory_service=message_factory_service,
    )

    identify_callback_query_use_case_config = providers.Singleton(IdentifyCallbackQueryUseCaseConfig)
    identify_callback_query_use_case = providers.Factory(
        IdentifyCallbackQueryUseCase,
        command_repository=command_repository,
        config=identify_callback_query_use_case_config,
    )

    handle_awaiting_answer_callback_use_case = providers.Factory(
        HandleAwaitingAnswerCallbackUseCase,
        guest_form_repository=guest_form_repository,
    )
    handle_invitation_neediness_callback_use_case = providers.Factory(
        HandleInvitationNeedinessCallbackUseCase,
        guest_form_repository=guest_form_repository,
        invitation_request_repository=invitation_request_repository,
    )
    handle_address_input_use_case = providers.Factory(
        HandleAddressInputCallbackUseCase,
        guest_form_repository=guest_form_repository,
        invitation_request_repository=invitation_request_repository,
        get_address_by_location_service=get_address_by_location_service,
    )
    handle_geotag_validation_callback_use_case = providers.Factory(
        HandleGeotagValidationCallbackUseCase,
        guest_form_repository=guest_form_repository,
        invitation_request_repository=invitation_request_repository,
    )
    handle_address_specification_callback_use_case = providers.Factory(
        HandleAddressSpecificationCallbackUseCase,
        guest_form_repository=guest_form_repository,
        invitation_request_repository=invitation_request_repository,
    )
    handle_additional_info_callback_use_case = providers.Factory(
        HandleAdditionalInfoCallbackUseCase,
        guest_form_repository=guest_form_repository,
    )

    # Applications
    bot_config = providers.Singleton(BotConfig)
    bot = providers.Singleton(AsyncTeleBot, token=bot_config().TOKEN)

    reply_markup_factory = providers.Factory(ReplyMarkupFactory)
    send_message_service = providers.Factory(SendMessageService)
