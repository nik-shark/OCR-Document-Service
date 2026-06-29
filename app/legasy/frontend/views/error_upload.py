from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter()


@router.get(
    "/api/upload/error",
    response_class=HTMLResponse,
    name='error_upload_view')
async def error_upload_doc_temp(request: Request):
    data = {
        'name_page': 'error upload',
        'title': 'Ошибка добавления файла'
    }

    return templates.TemplateResponse(
        request=request,
        name="error_upload.html",
        context=data
    )