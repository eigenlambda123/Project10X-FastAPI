from time import sleep
from sqlalchemy.orm import Session
from app.db import sync_engine
from app.models import Task
from app.celery_app import celery
from celery import shared_task
import requests


@shared_task(
    bind=True,  
    name="long_task",
    autoretry_for=(Exception,), # Automatically retry on exceptions
    retry_kwargs={"max_retries": 3, "countdown": 5},  # Retry up to 3 times with a 5-second delay
)
def long_task(self, task_id: str, x: int):
    """
    Run a long task that simulates work by sleeping for 3 seconds
    and then updates the task status in the database.
    """
    with Session(sync_engine) as session:
        task = session.get(Task, task_id)
        if not task:
            return

        try:
            task.status = "STARTED"
            session.commit()

            sleep(3)  # Simulate work
            result = f"Result is {x * 2}"

            task.status = "SUCCESS"
            task.result = result
            session.commit()

            # Fire webhook if it exists
            if task.webhook_url:
                try:
                    # Notify the client by sending a POST request to the provided webhook URL with the task result
                    requests.post(task.webhook_url, json={"task_id": task.id, "result": result})
                except Exception as webhook_error:
                    print("Webhook failed:", webhook_error)

        except Exception as e:
            task.status = "FAILURE"
            task.result = str(e)
            session.commit()
            raise  # Triggers retry
