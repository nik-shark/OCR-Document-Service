from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(tags=['Success_delete_view'])


@router.get(
    "/api/delete/success",
    response_class=HTMLResponse,
    name='success_delete_view')
async def success_delete_doc_temp(request: Request):
    data = {
        'name_page': 'success delete',
        'title': 'Успешное удаление'
    }

    return templates.TemplateResponse(
        request=request,
        name="success_delete.html",
        context=data
    )