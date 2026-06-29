from fastapi import APIRouter, File, UploadFile, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas import UploadResponse
from db.engine import get_db
from services.upload import doc_upload

router = APIRouter(prefix="/api")


@router.post('/upload',
             response_model=UploadResponse,
             status_code=status.HTTP_201_CREATED,
             summary='Upload documents',
             description="Uploads an image to MinIO and add information's in the database.",
             responses= {400: {'description': 'Invalid request'}}
             )

async def upload_doc(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):

    return await doc_upload(file, db)
