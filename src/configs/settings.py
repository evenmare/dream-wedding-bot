"""Module contains application settings."""

from functools import lru_cache
from pathlib import Path

from pydantic import computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
    """Base application configuration class."""

    SRC_DIR: Path = Path(__file__).parent.parent
    BASE_DIR: Path = SRC_DIR.parent
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


class CacheSettings(BaseAppSettings):
    """Redis connection configuration."""

    CACHE_HOST: str = Field(alias='REDIS_HOST')
    CACHE_PORT: str = Field(alias='REDIS_PORT')
    CACHE_NAME: str = Field(
        alias='REDIS_DB',
        default='0',
    )
    CACHE_USER: str = Field(
        alias='REDIS_USER',
        default='',
    )
    CACHE_PASSWORD: str = Field(
        alias='REDIS_PASSWORD',
        default='',
    )

    @computed_field
    @property
    def url(self) -> str:
        return (
            f'redis://{self.CACHE_USER}:{self.CACHE_PASSWORD}@'
            f'{self.CACHE_HOST}:{self.CACHE_PORT}/{self.CACHE_NAME}'
        )


class DbSettings(BaseAppSettings):
    """Database connection configuration."""

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str = Field(alias='POSTGRES_DB')
    DB_USER: str = Field(alias='POSTGRES_USER')
    DB_PASSWORD: str = Field(alias='POSTGRES_PASSWORD')

    @computed_field
    @property
    def url(self) -> str:
        return (
            f'asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )


@lru_cache
def get_cache_settings() -> CacheSettings:
    """Retrieve cache settings."""
    return CacheSettings()


cache_settings: CacheSettings = get_cache_settings()


@lru_cache
def get_db_settings() -> DbSettings:
    """Retrieve database settings."""
    return DbSettings()


db_settings: DbSettings = get_db_settings()
