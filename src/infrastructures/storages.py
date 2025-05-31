"""Module contains storage infrastractures."""

from typing import AsyncGenerator

from aiobotocore.session import AioSession
from aiobotocore.client import AioBaseClient

from configs.infrastractures import StorageConfig


async def get_s3_client(
    session: AioSession,
    config: StorageConfig,
) -> AsyncGenerator[AioBaseClient, None]:
    """Generates S3 client.

    :param session: Aiobotocore session.
    :param service_name: Service name.
    :param aws_access_key_id: Access Key.
    :param aws_secret_access_key: Secret Key.
    :yield: Async S3 client.
    """
    async with session.create_client(
        service_name='s3',
        endpoint_url=config.ENDPOINT_URL,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    ) as client:
        yield client
