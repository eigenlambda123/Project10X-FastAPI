import asyncio
from uuid import UUID

import os
import json

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


async def generate_report(task_id: UUID, data: dict):
    """Async task for Generating a report based on provided data"""
    try:
        print(f"[{task_id}] Generating report...")
        await asyncio.sleep(3)  # Simulate longer task
        print(f"[{task_id}] Report generated for: {data}")
        update_task_status(task_id, status="success", result={"report": f"Report for {data}"}) # Update task status successfully
    except Exception as e:
        update_task_status(task_id, status="failed", error=str(e)) # Update task status on failure



async def generate_file(task_id: UUID, content: dict):
    """Async task for Generating JSON file from content"""
    try:
        await asyncio.sleep(2) # Simulate file generation delay

        # Ensure output dir
        os.makedirs("outputs", exist_ok=True) # Create outputs directory if it doesn't exist

        file_path = f"outputs/{task_id}.json" # Define the file path for the output JSON file

        # Write content to JSON file
        with open(file_path, "w") as f:
            json.dump(content, f, indent=2)

        result = {"file_path": file_path} # Result containing the file path
        update_task_status(task_id, "success", result=result) # Update task status successfully
        
    except Exception as e:
        update_task_status(task_id, "failed", error=str(e))