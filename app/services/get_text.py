from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import DocumentsModel


async def get_recognized_text(item_id: int, db: AsyncSession):
    text = await db.execute(
        select(DocumentsModel)
        .options(selectinload(DocumentsModel.text))
        .where(DocumentsModel.id == item_id)
    )

    db_item = text.scalar_one_or_none()

    if not db_item:
        raise HTTPException(
            status_code=404,
            detail='Text not found',
        )

    return db_item.text