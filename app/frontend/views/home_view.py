from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse, name='home_view')
async def read_root(request: Request):
    data = {
        'name_page': 'home',
        'title': 'Главная страница'
    }

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=data
    )
