"""Module contains infrastractures tests."""

from collections.abc import AsyncGenerator

import pytest
from tortoise import Tortoise
from tortoise.contrib.test import _init_db, getDBConfig, truncate_all_models

from configs.settings import get_db_settings

db_settings = get_db_settings()


@pytest.fixture(scope='session')
def db_url() -> str:
    """Database URL"""
    return f'asyncpg://{db_settings.DB_USER}:{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:{db_settings.DB_PORT}/test'


@pytest.fixture(scope='session')
async def db(
    request: pytest.FixtureRequest,
    db_url: str,
) -> AsyncGenerator[None, None]:
    """Database initialization"""
    config = getDBConfig(
        app_label=db_settings.app_name,
        modules=db_settings.models,
    )

    await _init_db(config)
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope='function', autouse=True)
async def truncate_db(db: AsyncGenerator[None, None]) -> AsyncGenerator[None, None]:
    """Truncate database after test"""
    yield
    await truncate_all_models()
