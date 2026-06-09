from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.upload import router as upload_router
from api.delete import router as delete_router
from api.get_text import router as get_text_router
from api.analyse import router as analyse_router

from core.engine import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(upload_router)
app.include_router(delete_router)
app.include_router(get_text_router)
app.include_router(analyse_router)
