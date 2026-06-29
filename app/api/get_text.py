from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from services.get_text import get_recognized_text
from schemas.schemas import GetResponse

router = APIRouter(prefix="/api")


@router.get('/text',
            response_model=GetResponse,
             summary='Get text',
             description="Get recognized text from database."
             )

async def get_text(item_id: int, db: AsyncSession = Depends(get_db)):
    return await get_recognized_text(item_id, db)