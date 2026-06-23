from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from minio import S3Error
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from db.models import DocumentsModel
from services.tesseract_analyse import document_analyse
'''
     Апи должна принимать id документа и вызывать функцию очереди задач celery для выполнения в
    фоновом режиме. В методе celery необходимо вызвать библиотеку tesseract для получения текста и записать результат в
    Documents_text. Вам здесь понадобиться брокер сообщений, например RabbitMQ.
'''
router = APIRouter(prefix="/api")

'''
5. Создать Celery-задачу
   Создать обычную функцию, не async def.
   Например, логически она называется:
   analyse_document(document_id)
   Внутри она должна:
   Получить документ из БД по ID.✅
   Получить путь к его изображению.
   Открыть изображение через Pillow.
   Передать его в pytesseract.
   Получить распознанный текст.
   Записать текст в таблицу Documents_text.
   Сохранить изменения в БД.
'''

# TODO изменить template delete/error на стандартный 404 для всего
@router.post('/analyse/{item_id}')
async def doc_analyse(item_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(DocumentsModel).where(
            DocumentsModel.id == item_id,
        )
    )

    db_item = result.scalar_one_or_none()

    if db_item is None:
        return RedirectResponse(
            url="delete/error",
            status_code=404,
        )

    try:
        await document_analyse(db_item.path)

    except S3Error:
        raise HTTPException(
            status_code=500,
            detail="S3 error"
        )





    # await db.delete(db_item)
    # await db.commit()
    #
    # return RedirectResponse(
    #     url="delete/success",
    #     status_code=303,
    # )
    #
    #





