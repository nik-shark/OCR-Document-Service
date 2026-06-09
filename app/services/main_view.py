from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from typing import Optional, List, Dict, Annotated
from sqlalchemy import select

from db.models import DocumentsModel, DocumentsTextModel
from core.engine import AsyncSessionLocal, engine, Base, get_db
from schemas.schemas import Documents, DocumentsText


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    lifespan=lifespan
)





@app.post('/analyse')
async def doc_analyse():
    return f"""
        Апи должна принимать id документа и вызывать функцию очереди задач celery для выполнения в
    фоновом режиме. В методе celery необходимо вызвать библиотеку tesseract для получения текста и записать результат в
    Documents_text. Вам здесь понадобиться брокер сообщений, например RabbitMQ.
    """




