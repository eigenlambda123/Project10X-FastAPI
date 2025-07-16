import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_submit_task():
    """
    Test the task submission endpoint
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/tasks/submit", json={})
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data

