from uuid import UUID
from datetime import datetime
from typing import Optional

# Global in-memory task registry
task_store: dict[UUID, dict] = {}

def create_task_entry(task_id: UUID, task_type: str, data: dict):
    """Create a new task entry in the task store"""

    task_store[task_id] = {
        "status": "pending",
        "type": task_type,
        "data": data,
        "result": None,
        "error": None,
        "timestamp": datetime.utcnow(),
        "retries": 0
    }

def update_task_status(task_id: UUID, status: str, result=None, error=None):
    """Update the status of a task in the task store"""

    task = task_store.get(task_id)
    if task:
        task["status"] = status
        task["result"] = result
        task["error"] = error

def get_task(task_id: UUID) -> Optional[dict]:
    """Retrieve a task by ID from the task store"""
    return task_store.get(task_id)
