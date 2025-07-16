import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_submit_task():
    """
    Test the task submission endpoint
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/tasks/submit", json={})
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data


async def test_task_status(client):
    """
    Test the task status endpoint
    """
    response = await client.post("/tasks/submit", json={})
    task_id = response.json()["task_id"]

    status = await client.get(f"/tasks/{task_id}/status")
    assert status.status_code == 200
    assert status.json()["status"] in ["PENDING", "STARTED", "SUCCESS"]


