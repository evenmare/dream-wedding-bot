"""Module contains repositories configs implementations."""

from configs.base import BaseAppSettings


class StorageRepositoryConfig(BaseAppSettings):
    """Config for StorageRepository."""

    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'S3_REPOSITORY_',
    }

    BUCKET: str
