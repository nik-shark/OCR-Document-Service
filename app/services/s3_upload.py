from uuid import uuid4
from io import BytesIO

from fastapi import UploadFile

from services.s3_settings import client, BUCKET_NAME


def create_bucket_if_not_exists():
    found = client.bucket_exists(BUCKET_NAME)

    if not found:
        client.make_bucket(BUCKET_NAME)


async def upload_file_to_s3(file: UploadFile) -> str:
    create_bucket_if_not_exists()

    file_data = await file.read()

    file_name = f"{uuid4()}_{file.filename}"

    client.put_object(
        bucket_name=BUCKET_NAME,
        object_name=file_name,
        data=BytesIO(file_data),
        length=len(file_data),
        content_type=file.content_type,
    )

    return file_name