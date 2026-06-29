from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.analyse import start_document_analyse


@pytest.mark.anyio
async def test_start_document_analyse_success():
    db = AsyncMock(spec=AsyncSession)

    document = Mock()
    document.id = 10
    document.path = "stored-image.jpg"

    query_result = Mock()
    query_result.scalar_one_or_none.return_value = document
    db.execute.return_value = query_result

    celery_result = Mock()
    celery_result.id = "task-123"

    celery_task = Mock()
    celery_task.delay.return_value = celery_result

    get_image = AsyncMock(return_value=b"image bytes")

    with (
        patch(
            "services.analyse.get_img_from_s3",
            get_image,
        ),
        patch(
            "services.analyse.image_to_text_task",
            celery_task,
        ),
    ):
        result = await start_document_analyse(
            item_id=document.id,
            db=db,
        )

    assert result == {
        "status": 200,
        "task_id": "task-123",
        "document_id": 10,
    }

    db.execute.assert_awaited_once()
    query_result.scalar_one_or_none.assert_called_once_with()

    get_image.assert_awaited_once_with(
        "stored-image.jpg"
    )

    celery_task.delay.assert_called_once_with(
        10,
        b"image bytes",
    )


@pytest.mark.anyio
async def test_start_document_analyse_not_found():
    db = AsyncMock(spec=AsyncSession)

    query_result = Mock()
    query_result.scalar_one_or_none.return_value = None
    db.execute.return_value = query_result

    get_image = AsyncMock()
    celery_task = Mock()

    with (
        patch(
            "services.analyse.get_img_from_s3",
            get_image,
        ),
        patch(
            "services.analyse.image_to_text_task",
            celery_task,
        ),
    ):
        with pytest.raises(HTTPException) as exc:
            await start_document_analyse(
                item_id=999_999_999,
                db=db,
            )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Image for recognize not found."

    db.execute.assert_awaited_once()

    get_image.assert_not_awaited()
    celery_task.delay.assert_not_called()


@pytest.mark.anyio
async def test_analyse_does_not_start_task_when_minio_fails():
    db = AsyncMock(spec=AsyncSession)

    document = Mock()
    document.id = 10
    document.path = "missing-image.jpg"

    query_result = Mock()
    query_result.scalar_one_or_none.return_value = document
    db.execute.return_value = query_result

    celery_task = Mock()

    with (
        patch(
            "services.analyse.get_img_from_s3",
            AsyncMock(side_effect=RuntimeError("MinIO unavailable")),
        ),
        patch(
            "services.analyse.image_to_text_task",
            celery_task,
        ),
    ):
        with pytest.raises(RuntimeError, match="MinIO unavailable"):
            await start_document_analyse(
                item_id=document.id,
                db=db,
            )

    celery_task.delay.assert_not_called()
