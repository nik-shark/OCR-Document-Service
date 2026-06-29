import logging
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DocumentsModel
from tasks import image_to_text_task
from services.s3_operations import get_img_from_s3

logger = logging.getLogger(__name__)


async def start_document_analyse(item_id: int, db: AsyncSession):
    result = await db.execute(
        select(DocumentsModel).where(
            DocumentsModel.id == item_id,
        )
    )

    db_item = result.scalar_one_or_none()

    if db_item is None:
        logger.warning('Document not found: document_id=%s', item_id)

        raise HTTPException(
            status_code=404,
            detail='Image for recognize not found.'
        )

    img_bytes = await get_img_from_s3(db_item.path)

    task = image_to_text_task.delay(db_item.id, img_bytes)

    return {
        'status': 200,
        'task_id': task.id,
        'document_id': db_item.id,
    }

