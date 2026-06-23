from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from services.delete import delete_doc

router = APIRouter(prefix="/api")


@router.delete('/delete')
async def doc_delete(
        item_id: int,
        db: AsyncSession = Depends(get_db)
):

    return await delete_doc(item_id, db)