from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(tags=['Get_text_view'])


@router.get("/get", response_class=HTMLResponse, name='get_text_view')
async def get_text_temp(request: Request):
    data = {
        'name_page': 'get text',
        'title': 'Получение текста'
    }

    return templates.TemplateResponse(
        request=request,
        name="get_text.html",
        context=data
    )
