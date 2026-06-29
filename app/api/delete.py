from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from services.delete import delete_doc

router = APIRouter(prefix="/api")


@router.delete('/delete',
               summary='Delete document',
               description='Delete document from MinIO and from database.',
               status_code=status.HTTP_204_NO_CONTENT,
               responses={404: {'description': 'Not Found'}}
               )

async def doc_delete(
        item_id: int,
        db: AsyncSession = Depends(get_db)
):

    return await delete_doc(item_id, db)