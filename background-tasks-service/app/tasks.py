import asyncio
from uuid import UUID

from app.store import update_task_status

async def send_notification(task_id: UUID, email: str, message: str):
    """Async task for Sending a notification to a user via email"""
    try:
        print(f"[{task_id}] Starting send_notification task...")
        await asyncio.sleep(2) # Simulate sending delay
        print(f"[{task_id}] Sent notification to {email}: {message}")
        update_task_status(task_id, status="success", result={"delivered_to": email}) # Update task status successfully
    except Exception as e:
        update_task_status(task_id, status="failed", error=str(e)) # Update task status on failure