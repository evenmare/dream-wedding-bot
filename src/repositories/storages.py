"""Module contains implementation of storage repository."""

from typing import TYPE_CHECKING

from configs.repositories import StorageRepositoryConfig

if TYPE_CHECKING:
    from types_aiobotocore_s3.client import S3Client


class StorageRepository:
    """Class contains repository for storage access."""

    def __init__(
        self,
        client: 'S3Client',
        config: StorageRepositoryConfig,
    ):
        """Class constructor.

        :param s3_client: Client of S3 Session.
        :param config: Settings for repository.
        """
        self.__client = client
        self.config = config

    async def get_file(self, filename: str) -> bytes:
        """Get file from storage.

        :param filename: Name of file.
        :return: Bytes of file.
        """
        response = await self.__client.get_object(
            Bucket=self.config.BUCKET,
            Key=filename,
        )
        return await response['Body'].read()

    async def put_file(self, filename: str, data: bytes) -> None:
        """Put file into storage.

        :param filename: Name of file.
        :param data: Data of file.
        """
        await self.__client.put_object(
            Bucket=self.config.BUCKET,
            Key=filename,
            Body=data,
        )

    async def healthcheck(self) -> None:
        """Check health of connection."""
        await self.__client.head_bucket(Bucket=self.config.BUCKET)
