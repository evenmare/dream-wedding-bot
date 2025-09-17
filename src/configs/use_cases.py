"""Module contains Use Case's config implementations."""
from configs.base import BaseAppSettings


class IdentifyCallbackQueryUseCaseConfig(BaseAppSettings):
    """Config for HandleCallbackQueryUseCase."""

    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'HANDLE_CALLBACK_QUERY_',
    }

    DEFAULT_COMMAND_CODE: str = 'menu'
