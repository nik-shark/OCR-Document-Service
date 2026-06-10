from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(tags=['Upload_view'])


@router.get("/upload", response_class=HTMLResponse, name='upload_view')
async def upload_doc_temp(request: Request):
    data = {
        'name_page': 'upload documents',
        'title': 'Загрузка документов'
    }

    return templates.TemplateResponse(
        request=request,
        name="upload.html",
        context=data
    )