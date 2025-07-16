import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import pytest_asyncio
import asyncio

@pytest_asyncio.fixture
async def client():
    """
    Fixture to create an HTTP client for testing FastAPI endpoints
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_submit_task():
    """
    Test the task submission endpoint
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/tasks/submit", json={})
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data


@pytest.mark.asyncio
async def test_task_status(client):
    """
    Test the task status endpoint
    """
    response = await client.post("/api/tasks/submit", json={})
    task_id = response.json()["task_id"]

    status = await client.get(f"/api/tasks/{task_id}/status")
    assert status.status_code == 200
    assert status.json()["status"] in ["PENDING", "STARTED", "SUCCESS"]


@pytest.mark.asyncio
async def test_task_result(client):
    """
    Test the task result endpoint
    """
    # Submit a task
    response = await client.post("/api/tasks/submit", json={})
    assert response.status_code == 200

    # extract task_id from the response
    task_id = response.json()["task_id"]
    await asyncio.sleep(5)

    # check the result if its returning 200 or 404
    response = await client.get(f"/api/tasks/{task_id}/result")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert "result" in response.json()



