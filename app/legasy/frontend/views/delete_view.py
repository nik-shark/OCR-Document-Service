from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter()


@router.get("/delete", response_class=HTMLResponse, name='delete_view')
async def delete_doc_temp(request: Request):
    data = {
        'name_page': 'delete documents',
        'title': 'Удаление документов'
    }

    return templates.TemplateResponse(
        request=request,
        name="delete.html",
        context=data
    )
