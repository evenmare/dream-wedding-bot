"""Module contains database infrastructure implementation."""

from configs.settings import get_db_settings

db_settings = get_db_settings()

TORTOISE_ORM = {
    'connections': {
        'default': db_settings.url,
    },
    'apps': {
        'dream_wedding_bot': {
            'models': [
                'entities.database.guests',
                'entities.database.invitations',
                'entities.database.telegram',
                'aerich.models',
            ],
            'default_connection': 'default',
        },
    },
}
