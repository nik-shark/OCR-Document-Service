import logging
import os
from celery import Celery

from logging_setting import setup_logging

setup_logging(service_name='worker')
logger = logging.getLogger(__name__)

broker_url = os.getenv("RABBITMQ_URL")

if not broker_url:
    logger.critical('RABBITMQ_URL is not configured')
    raise RuntimeError("RABBITMQ_URL not found")


celery_app = Celery(
    "documents",
    broker=broker_url,
    include=["tasks"],
)

celery_app.conf.update(
    worker_hijack_root_logger=False,
    worker_redirect_stdouts=False,
)

logger.info("Celery application configured")