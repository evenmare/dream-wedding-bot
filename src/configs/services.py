"""Module contains services configs implementations."""

from pydantic import Field
from configs.base import BaseAppSettings
from typings.services import LANGUAGE_RFC2616_REGEXP


class GetAddressByLocationServiceConfig(BaseAppSettings):
    """Settings for GetAddressByLocationService."""

    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'ADDRESS_BY_LOCATION_SERVICE_',
    }

    LANGUAGE_CODE: str = Field(pattern=LANGUAGE_RFC2616_REGEXP)


class MessageFactoryServiceConfig(BaseAppSettings):
    """Settings for MessageFactoryService."""

    model_config = {
        **BaseAppSettings.model_config,
        'env_prefix': 'MESSAGE_FACTORY_SERVICE_',
    }

    BASE_FILES_URL: str