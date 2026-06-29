from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException
from pathlib import Path

from services.delete import delete_doc
from db.models import DocumentsModel

TEST_FILES_DIR = Path(__file__).resolve().parent / 'test_files'


@pytest.mark.anyio
async def test_success_delete_img(client):
    image_path = TEST_FILES_DIR / "first_img.jpg"

    with image_path.open("rb") as image:
        upload_response = await client.post(
            "/api/upload",
            files={
                "file": (
                    image_path.name,
                    image,
                    "image/jpeg",
                )
            },
        )

    assert upload_response.status_code == 201

    document_id = upload_response.json()["id"]

    delete_response = await client.delete(
        "/api/delete",
        params={"item_id": document_id},
    )

    assert delete_response.status_code == 204


@pytest.mark.anyio
async def test_delete_document_not_found():
    db = AsyncMock()

    result = Mock()
    result.scalar_one_or_none.return_value = None
    db.execute.return_value = result

    with pytest.raises(HTTPException) as exc:
        await delete_doc(
            item_id=999_999_999,
            db=db,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Document for delete not found."

    db.execute.assert_awaited_once()


@pytest.mark.anyio
async def test_delete_document_not_found_in_minio():
    db = AsyncMock()

    result = Mock()
    result.scalar_one_or_none.return_value = None
    db.execute.return_value = result

    with pytest.raises(HTTPException) as exc:
        await delete_doc(
            item_id=999_999_999,
            db=db,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Document for delete not found."

    db.execute.assert_awaited_once()


@pytest.mark.anyio
async def test_minio_delete_error_does_not_delete_from_db():
    db = AsyncMock()

    document = Mock()
    document.id = 10
    document.path = "image.jpg"

    result = Mock()
    result.scalar_one_or_none.return_value = document
    db.execute.return_value = result

    minio_delete = AsyncMock(return_value=False)

    with patch(
            "services.delete.delete_file_to_s3",
            minio_delete,
    ):
        with pytest.raises(HTTPException) as exc:
            await delete_doc(
                item_id=document.id,
                db=db,
            )

    assert exc.value.status_code == 500
    assert exc.value.detail == "S3 delete error"

    minio_delete.assert_awaited_once_with(document.path)

    # Самые важные проверки:
    db.delete.assert_not_awaited()
    db.commit.assert_not_awaited()
