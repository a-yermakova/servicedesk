from app.core.config import settings
from celery import Celery

C_FORCE_ROOT = 1
redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"

celery_app = Celery(
    "celery_worker",
    broker=redis_url,
    backend=redis_url
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,
    timezone='Europe/Moscow',
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    include="app.email.tasks",
)

celery_app.conf.task_routes = {
    "app.email.tasks.process_new_email_task": {"queue": "email_queue"},
}
