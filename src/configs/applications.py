"""Module contains settings for applications."""

from configs.base import BaseAppSettings


class BotConfig(BaseAppSettings):
    """Config for bot."""

    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'BOT_',
    }

    TOKEN: str


class MessageConfig(BaseAppSettings):
    """Config for bot messages."""

    model_config = {
        **BaseAppSettings.model_computed_fields,
        'env_prefix': 'BOT_MESSAGES_',
    }

    INLINE_KEYBOARD_ROW_WIDTH: int
