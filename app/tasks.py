import asyncio
import logging
from io import BytesIO

import pytesseract
from PIL import Image

from db.engine import AsyncSessionLocal
from celery_app import celery_app
from db.models import DocumentsTextModel

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name='image_to_text_task')
def image_to_text_task(self, item_id, img_bytes: bytes) -> str:
    logger.info(
        'OCR task started: task_id=%s document_id=%s',
        self.request.id,
        item_id,
    )

    try:
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

        logger.info(
            'OCR task completed: task_id=%s document_id=%s',
            self.request.id,
            item_id,
        )

        return text

    except Exception:
            logger.exception(
                'OCR task failed: task_id=%s document_id=%s',
                self.request.id,
                item_id
            )
            raise

async def save_text_db(doc_id: int, text: str):
    async with AsyncSessionLocal() as db:
        doc_text = DocumentsTextModel(
            doc_id=doc_id,
            text=text
        )

        db.add(doc_text)
        await db.commit()