from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from minio import S3Error
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DocumentsModel
from core.engine import get_db
from services.s3_delete import delete_file_to_s3

router = APIRouter(tags=['Delete'], prefix="/api")

@router.get('/delete')
async def doc_delete(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DocumentsModel).where(
            DocumentsModel.id == item_id
        )
    )

    db_item = result.scalar_one_or_none()

    if not db_item:
        return RedirectResponse(
            url="delete/error",
            status_code=303,
        )

    try:
        await delete_file_to_s3(db_item.path)

    except S3Error:
        raise HTTPException(
            status_code=500,
            detail="S3 delete error"
        )

    await db.delete(db_item)
    await db.commit()

    return RedirectResponse(
        url="delete/success",
        status_code=303,
    )