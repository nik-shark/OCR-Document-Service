from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DocumentsModel
from services.s3_operations import delete_file_to_s3


async def delete_doc(item_id: int, db: AsyncSession):
    result = await db.execute(
        select(DocumentsModel).where(
            DocumentsModel.id == item_id
        )
    )

    db_item = result.scalar_one_or_none()

    if not db_item:
        raise HTTPException(
            status_code=404,
            detail='Image for delete not found.'
        )

    is_deleted = await delete_file_to_s3(db_item.path)

    if not is_deleted:
        raise HTTPException(
            status_code=500,
            detail="S3 delete error"
        )

    await db.delete(db_item)
    await db.commit()

    return {
        'status': 204,
        "document_id": db_item.id,
    }