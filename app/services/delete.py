import logging
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DocumentsModel
from services.s3_operations import delete_file_to_s3

logger = logging.getLogger(__name__)


async def delete_doc(item_id: int, db: AsyncSession):
    result = await db.execute(
        select(DocumentsModel).where(
            DocumentsModel.id == item_id
        )
    )

    db_item = result.scalar_one_or_none()

    if not db_item:
        logger.warning(
            'Document for delete not found: document_id=%s',
            item_id
        )

        raise HTTPException(
            status_code=404,
            detail='Document for delete not found.'
        )

    is_deleted = await delete_file_to_s3(db_item.path)

    if not is_deleted:
        logger.exception('MinIO delete operation failed')

        raise HTTPException(
            status_code=500,
            detail="S3 delete error"
        )

    logger.info(
        'Document was delete from MinIO and from databse: document_id=%s',
                item_id
                )

    await db.delete(db_item)
    await db.commit()

    return {
        'status': 204,
        "document_id": db_item.id,
    }