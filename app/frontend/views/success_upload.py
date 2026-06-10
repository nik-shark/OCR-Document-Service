from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(tags=['Success_upload_view'])


@router.get(
    "/api/upload/success",
    response_class=HTMLResponse,
    name='success_upload_view')
async def success_upload_doc_temp(request: Request):
    data = {
        'name_page': 'success upload',
        'title': 'Успешная загрузка'
    }

    return templates.TemplateResponse(
        request=request,
        name="success_upload.html",
        context=data
    )