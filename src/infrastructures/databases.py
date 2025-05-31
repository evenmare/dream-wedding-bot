"""Module contains database infrastructure implementation."""

from tortoise import Tortoise
from configs.infrastractures import DbConfig

db_settings = DbConfig()

TORTOISE_ORM = {
    'connections': {
        'default': db_settings.url,
    },
    'apps': {
        db_settings.app_name: {
            'models': db_settings.models,
            'default_connection': 'default',
        },
    },
}


async def init_db() -> None:
    """Initialize database connection."""
    await Tortoise.init(config=TORTOISE_ORM)
