"""Module contains infrastractures configs implementations."""

from pydantic import Field

from configs.base import BaseAppSettings


class DbConfig(BaseAppSettings):
    """Database connection configuration."""

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str = Field(alias='POSTGRES_DB')
    DB_USER: str = Field(alias='POSTGRES_USER')
    DB_PASSWORD: str = Field(alias='POSTGRES_PASSWORD')

    @property
    def url(self) -> str:
        """Database URL."""
        return f'asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def app_name(self) -> str:
        """App name for Tortoise."""
        return 'dream_wedding_bot'

    @property
    def models(self) -> list[str]:
        """Models list."""
        return [
            'entities.database.commands',
            'entities.database.callbacks',
            'entities.database.notifications',
            'entities.database.telegram',
            'entities.database.forms',
            'entities.database.invitations',
            'entities.database.guests',
            'aerich.models',
        ]


class StorageConfig(BaseAppSettings):
    """Storage connection settings."""

    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'S3_',
    }

    SERVICE_NAME: str = Field(default='dream_wedding_bot')
    ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str


class GeocoderConfig(BaseAppSettings):
    """Geocoder connection settings."""

    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'GEOCODER_',
    }

    USER_AGENT: str = Field(serialization_alias='user_agent')
