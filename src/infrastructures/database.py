"""Module contains database infrastructure implementation."""

from configs.settings import get_db_settings

db_settings = get_db_settings()

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
