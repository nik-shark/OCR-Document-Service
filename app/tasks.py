import asyncio
import pytesseract
from io import BytesIO
from PIL import Image
from db.engine import AsyncSessionLocal

from celery_app import celery_app
from db.models import DocumentsTextModel


@celery_app.task(name='image_to_text_task')
def image_to_text_task(item_id, img_bytes) -> str:
    img = Image.open(BytesIO(img_bytes))

    text = pytesseract.image_to_string(
        img,
        lang="rus+eng",
        config="--psm 3",
    )

    if not text.strip():
        raise ValueError('The text can not be recognized')

    worker_loop = asyncio.new_event_loop()

    worker_loop.run_until_complete(save_text_db(item_id, text))

    return text


async def save_text_db(doc_id: int, text: str):
    async with AsyncSessionLocal() as db:
        doc_text = DocumentsTextModel(
            doc_id=doc_id,
            text=text
        )

        db.add(doc_text)
        await db.commit()