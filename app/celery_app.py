import os

from celery import Celery

broker_url = os.getenv("RABBITMQ_URL")

if not broker_url:
    raise RuntimeError("Переменная RABBITMQ_URL не задана")

celery_app = Celery(
    "documents",
    broker=broker_url,
    include=["tasks"],
)