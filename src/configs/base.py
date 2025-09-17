"""Module contains base config implementation."""

from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path


class BaseAppSettings(BaseSettings):
    """Base application configuration class."""

    SRC_DIR: Path = Path(__file__).parent.parent
    BASE_DIR: Path = SRC_DIR.parent
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )
