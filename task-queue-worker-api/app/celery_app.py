from celery import Celery

# Celery setup with Redis as broker and backend
celery = Celery(
    "task_queue_worker_api",
    broker="redis://localhost:6379/0",  
    backend="redis://localhost:6379/0"
)

celery.autodiscover_tasks(["app.worker"])