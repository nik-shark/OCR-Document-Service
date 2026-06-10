from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter(tags=['Analyse_view'])


@router.get("/analyse", response_class=HTMLResponse, name='analyse_view')
async def analyse_doc_temp(request: Request):
    data = {
        'name_page': 'analyse documents',
        'title': 'Анализ документов'
    }

    return templates.TemplateResponse(
        request=request,
        name="analyse.html",
        context=data
    )
