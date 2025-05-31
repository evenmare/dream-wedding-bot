"""Module contains settings for applications."""

from configs.base import BaseAppSettings


class BotConfig(BaseAppSettings):
    """Config for main bot."""

    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'BOT_',
    }

    TOKEN: str
