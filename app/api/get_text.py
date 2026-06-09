from fastapi import APIRouter


router = APIRouter(tags=['Upload'])

@router.get('/gettext')
async def get_text():
    return f"""
        Реализуйте {{API /get_text }}- Апи должна принимать id документа и возвращать текст из БД.
    """