from fastapi import APIRouter


router = APIRouter(tags=['Delete'])

@router.delete('/delete')
async def doc_delete():
    return f"""
        Реализуйте API /doc_delete — Апи должна принимать id документа и удалять его из базы данных и с диска.
    """