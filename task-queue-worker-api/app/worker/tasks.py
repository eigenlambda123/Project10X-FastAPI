from time import sleep
from sqlalchemy.orm import Session
from app.db import sync_engine
from app.models import Task
from app.celery_app import celery

@celery.task(name="long_task")
def long_task(task_id: str, x: int):
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

        except Exception as e:
            task.status = "FAILURE"
            task.result = str(e)
            session.commit()
