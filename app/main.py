from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.upload import router as upload_router
from api.delete import router as delete_router
from api.get_text import router as get_text_router
from api.analyse import router as analyse_router

from frontend.views.home_view import router as home_view
from frontend.views.upload_view import router as upload_view
from frontend.views.delete_view import router as delete_view
from frontend.views.get_text_view import router as get_text_view
from frontend.views.analyse_view import router as analyse_view
from frontend.views.success_upload import router as success_upload_view
from frontend.views.success_delete import router as success_delete_view
from frontend.views.error_upload import router as error_upload_view
from frontend.views.error_delete import router as error_delete_view

from core.engine import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


# ===== html templates ===== #
app.include_router(home_view)

app.include_router(upload_view)
app.include_router(delete_view)
app.include_router(get_text_view)
app.include_router(analyse_view)

app.include_router(success_upload_view)
app.include_router(success_delete_view)

app.include_router(error_delete_view)
app.include_router(error_upload_view)

# ===== api ===== #
app.include_router(upload_router)
app.include_router(delete_router)
app.include_router(get_text_router)
app.include_router(analyse_router)


# ===== mount static files ===== #
app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)