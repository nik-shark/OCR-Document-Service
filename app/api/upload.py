from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas import UploadResponse
from db.engine import get_db
from services.upload import doc_upload

router = APIRouter(prefix="/api")


@router.post('/upload', response_model=UploadResponse)
async def upload_doc(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):

    return await doc_upload(file, db)
