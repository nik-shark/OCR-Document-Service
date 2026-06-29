from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.s3_operations import (
    create_bucket_if_not_exists,
    delete_file_to_s3,
    get_img_from_s3,
    upload_file_to_s3,
)


def test_create_bucket_when_bucket_does_not_exist():
    with patch("services.s3_operations.client") as minio:
        minio.bucket_exists.return_value = False

        create_bucket_if_not_exists()

    minio.bucket_exists.assert_called_once_with("documents")
    minio.make_bucket.assert_called_once_with("documents")


def test_does_not_create_existing_bucket():
    with patch("services.s3_operations.client") as minio:
        minio.bucket_exists.return_value = True

        create_bucket_if_not_exists()

    minio.bucket_exists.assert_called_once_with("documents")
    minio.make_bucket.assert_not_called()


@pytest.mark.anyio
async def test_upload_file_to_s3():
    file = Mock()
    file.filename = "image.jpg"
    file.content_type = "image/jpeg"
    file.read = AsyncMock(return_value=b"image bytes")

    with (
        patch(
            "services.s3_operations.create_bucket_if_not_exists"
        ) as create_bucket,
        patch(
            "services.s3_operations.uuid4",
            return_value="fixed-uuid",
        ),
        patch("services.s3_operations.client") as minio,
    ):
        result = await upload_file_to_s3(file)

    assert result == "fixed-uuid_image.jpg"

    create_bucket.assert_called_once()
    file.read.assert_awaited_once()

    minio.put_object.assert_called_once()

    arguments = minio.put_object.call_args.kwargs

    assert arguments["bucket_name"] == "documents"
    assert arguments["object_name"] == "fixed-uuid_image.jpg"
    assert arguments["length"] == len(b"image bytes")
    assert arguments["content_type"] == "image/jpeg"
    assert arguments["data"].getvalue() == b"image bytes"


@pytest.mark.anyio
async def test_delete_file_from_s3_success():
    with patch("services.s3_operations.client") as minio:
        result = await delete_file_to_s3("image.jpg")

    assert result is True

    minio.remove_object.assert_called_once_with(
        bucket_name="documents",
        object_name="image.jpg",
    )


@pytest.mark.anyio
async def test_delete_file_from_s3_error():
    with patch("services.s3_operations.client") as minio:
        minio.remove_object.side_effect = RuntimeError(
            "MinIO unavailable"
        )

        result = await delete_file_to_s3("image.jpg")

    assert result is False

    minio.remove_object.assert_called_once_with(
        bucket_name="documents",
        object_name="image.jpg",
    )