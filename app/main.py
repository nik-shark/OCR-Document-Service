import logging
from contextlib import asynccontextmanager

from logging_setting import setup_logging

from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles

setup_logging(service_name="web")

# from legasy.frontend.views.home_view import router as home_view
# from legasy.frontend.views import router as upload_view
# from legasy.frontend.views import router as delete_view
# from legasy.frontend.views import router as get_text_view
# from legasy.frontend.views.analyse_view import router as analyse_view
# from legasy.frontend.views.success_upload import router as success_upload_view
# from legasy.frontend.views.success_delete import router as success_delete_view
# from legasy.frontend.views import router as error_upload_view
# from legasy.frontend.views import router as error_delete_view

from api.upload import router as upload_router
from api.delete import router as delete_router
from api.analyse import router as analyse_router
from api.get_text import router as get_text_router

from db.engine import engine, Base


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('OCR service begun')

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield
    except Exception:
        logger.exception('Fatal applications error')
        raise
    finally:
        await engine.dispose()
        logger.info('OCR service stopped')


app = FastAPI(lifespan=lifespan)

# ===== api ===== #
app.include_router(upload_router, tags=['api'])
app.include_router(analyse_router, tags=['api'])
app.include_router(get_text_router, tags=['api'])
app.include_router(delete_router, tags=['api'])


# # ===== html templates ===== #
# app.include_router(home_view, tags=['templates'])
# app.include_router(upload_view, tags=['templates'])
# app.include_router(delete_view, tags=['templates'])
# app.include_router(get_text_view, tags=['templates'])
# app.include_router(analyse_view, tags=['templates'])
#
# app.include_router(success_upload_view, tags=['templates'])
# app.include_router(error_upload_view, tags=['templates'])
#
# app.include_router(success_delete_view, tags=['templates'])
# app.include_router(error_delete_view, tags=['templates'])
#
#
# # ===== mount static files ===== #
# app.mount(
#     "/static",
#     StaticFiles(directory="frontend/static"),
#     name="static"
# )