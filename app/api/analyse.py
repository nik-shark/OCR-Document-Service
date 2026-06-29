from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from services.analyse import start_document_analyse

router = APIRouter(prefix="/api")


@router.post('/analyse',
             summary='Analyse documents',
             description="Analyse image and record information in database."
             )

async def document_analyse(
        item_id: int,
        db: AsyncSession = Depends(get_db)
):

    return await start_document_analyse(item_id, db)
