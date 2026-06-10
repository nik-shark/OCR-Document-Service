from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(tags=['Error_delete_view'])


@router.get(
    "/api/delete/error",
    response_class=HTMLResponse,
    name='error_delete_view')
async def error_delete_doc_temp(request: Request):
    data = {
        'name_page': 'error delete',
        'title': 'Ошибка удаления'
    }

    return templates.TemplateResponse(
        request=request,
        name="error_delete.html",
        context=data
    )