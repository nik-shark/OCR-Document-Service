import os
from celery import Celery


broker_url = os.getenv("RABBITMQ_URL")

if not broker_url:
    raise RuntimeError("RABBITMQ_URL not found")


celery_app = Celery(
    "documents",
    broker=broker_url,
    include=["tasks"],
)