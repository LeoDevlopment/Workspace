from contextlib import asynccontextmanager
from pathlib import Path
from uuid import UUID, uuid4

import aioboto3

from app.core.config import settings


class S3Service:
    def __init__(self) -> None:
        self._session = aioboto3.Session()

    @asynccontextmanager
    async def _client(self):
        async with self._session.client(
            "s3",
            endpoint_url=settings.MINIO_ENDPOINT,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            region_name=settings.MINIO_REGION,
        ) as client:
            yield client

    async def upload(self, key: str, data: bytes, content_type: str) -> None:
        async with self._client() as client:
            await client.put_object(
                Bucket=settings.MINIO_BUCKET,
                Key=key,
                Body=data,
                ContentType=content_type,
            )

    async def get_presigned_url(self, key: str, ttl: int | None = None) -> str:
        async with self._client() as client:
            url = await client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.MINIO_BUCKET, "Key": key},
                ExpiresIn=ttl or settings.PRESIGNED_URL_TTL,
            )
        if settings.MINIO_PUBLIC_ENDPOINT and settings.MINIO_ENDPOINT != settings.MINIO_PUBLIC_ENDPOINT:
            url = url.replace(settings.MINIO_ENDPOINT, settings.MINIO_PUBLIC_ENDPOINT)
        return url

    async def delete(self, key: str) -> None:
        async with self._client() as client:
            await client.delete_object(Bucket=settings.MINIO_BUCKET, Key=key)


def build_document_key(owner_type: str, owner_id: UUID, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return f"documents/{owner_type}/{owner_id}/{uuid4().hex}{ext}"


def build_workplace_photo_key(workplace_id: UUID, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return f"workplace-photos/{workplace_id}/{uuid4().hex}{ext}"


s3_service = S3Service()