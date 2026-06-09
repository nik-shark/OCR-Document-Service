from fastapi import APIRouter


router = APIRouter(tags=['Upload'])

@router.post('/upload')
async def upload_doc():
    return f"""
        Реализуйте API /upload_doc — загрузка документов. Апи должна принимать картинку в любом выбранном вами формате,
    загружать на S3 хранилище (можно использовать minio), и добавлять в базу запись в таблицу {{Documents, указав путь до
    сохраненного файла }}.
    """
