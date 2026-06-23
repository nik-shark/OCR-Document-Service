from fastapi import File, UploadFile, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services.s3_operations import upload_file_to_s3
from db.models import DocumentsModel
from db.engine import get_db

ALLOWED_EXTENSIONS = {"image/jpeg", "image/png"}


async def doc_upload(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    if file.content_type not in ALLOWED_EXTENSIONS:
        return RedirectResponse(
            url="upload/error",
            status_code=303,
        )

    file_path = await upload_file_to_s3(file)

    new_document = DocumentsModel(
        path=file_path
    )

    db.add(new_document)

    await db.commit()

    await db.refresh(new_document)

    return RedirectResponse(
        url="upload/success",
        status_code=303,
    )