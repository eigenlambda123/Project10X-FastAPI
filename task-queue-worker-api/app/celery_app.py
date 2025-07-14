from celery import Celery
from app.core.config import REDIS_URL

# Celery setup with Redis as broker and backend
celery = Celery(
    "task_queue_worker_api",
    broker=REDIS_URL,  
    backend=REDIS_URL
)

celery.autodiscover_tasks(["app.worker"])