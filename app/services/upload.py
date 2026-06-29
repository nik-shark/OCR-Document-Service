import logging
from fastapi import File, UploadFile, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.s3_operations import upload_file_to_s3
from db.models import DocumentsModel
from db.engine import get_db

ALLOWED_EXTENSIONS = {'image/jpeg', 'image/jpg', 'image/png'}

logger = logging.getLogger(__name__)


async def doc_upload(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    if file.content_type not in ALLOWED_EXTENSIONS:
        logger.warning('Unsupported file type')

        raise HTTPException(
            status_code=400,
            detail='Unsupported file type. Supported formats: JPEG, JPG, PNG.'
        )

    file_path = await upload_file_to_s3(file)

    new_document = DocumentsModel(
        path=file_path
    )

    logger.info('Document upload: document_id=%s', new_document.id)

    db.add(new_document)

    await db.commit()

    await db.refresh(new_document)

    return {
        "id": new_document.id,
        "path": new_document.path,
        "date": new_document.date
    }