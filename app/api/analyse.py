from fastapi import APIRouter


router = APIRouter(tags=['Get'])

@router.get('/analyse')
async def doc_analyse():
    return f"""
        Апи должна принимать id документа и вызывать функцию очереди задач celery для выполнения в
    фоновом режиме. В методе celery необходимо вызвать библиотеку tesseract для получения текста и записать результат в
    Documents_text. Вам здесь понадобиться брокер сообщений, например RabbitMQ.
    """