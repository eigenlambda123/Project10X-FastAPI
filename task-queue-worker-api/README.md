# About Task Queue Worker API

An async-ready task processing system built with **FastAPI**, **Celery**, and **Redis**.
This project demonstrates how to queue background jobs, track task status, return results, and trigger webhooks — all decoupled from the main API flow.

It showcases **event-driven task handling**, **worker architecture**, and real-world patterns like retry logic and callback notifications.

---

## Route Documentation

This API allows users to submit long-running background tasks, query their status or result, and optionally receive **asynchronous webhook notifications** upon task completion.

---

### **POST /api/tasks/submit**

**Description:** Submit a long-running background task.
Optionally accepts a `webhook_url` that will be notified when the task completes.

**Request Body:**

```json
{
  "webhook_url": "https://yourdomain.com/callback"  // (optional)
}
```

**Response:**

```json
{
  "task_id": "bd234e24-3af4-4ab2-8f9f-bc1a6cd77c95"
}
```

---

### **GET /api/tasks/{task\_id}/status**

**Description:** Check the current status of a submitted task.

**Response:**

```json
{
  "status": "PENDING"
}
```

---

### **GET /api/tasks/{task\_id}/result**

**Description:** Retrieve the result of a completed task, if available.

**Response (if successful):**

```json
{
  "result": "The task output here"
}
```

**Response (if not ready):**

```json
{
  "detail": "Result not available yet"
}
```

---

## Features

| Feature            | Description                                                          |
| ------------------ | -------------------------------------------------------------------- |
| Celery + Redis     | Queue background tasks using Redis as broker/backend                 |
| Task Submission    | Submit jobs via API and return a task ID immediately                 |
| Task Tracking      | Poll task status (`PENDING`, `STARTED`, `SUCCESS`, `FAILURE`)        |
| Result Retrieval   | View final output after task completion                              |
| Webhook Support    | Send `POST` notification to a callback URL once task completes       |
| Retry Logic        | Tasks automatically retry on failure with exponential backoff        |

---

## Models

* `Task`: Tracks submitted task ID, webhook URL (optional), and timestamps
* Celery task: A shared background function (e.g. `long_task(x)`) that simulates work
* No persistent business data — tasks and webhooks are the main concern

---

## Project Structure

```text
app/
├── main.py              # FastAPI app + route registration
├── celery_app.py        # Celery instance with Redis config
├── worker/
│   └── tasks.py         # Long-running Celery task definitions
├── db.py                # Async DB engine + session
├── models.py            # SQLModel class for Task
├── routers/
│   └── tasks.py         # API routes: submit, status, result
├── utils/
│   └── webhook.py       # Webhook POST logic
├── core/
│   └── config.py        # Load .env variables (DB + Redis)
```

---

## Notes

* Celery tasks are triggered using `.delay(...)` or `.apply_async(...)`
* Redis handles both task queueing (broker) and result tracking (backend)
* Webhooks are best-effort (fails silently if unreachable)
* Retries are automatic with exponential backoff using `autoretry_for` and `retry_backoff=True`
* Task lifecycle = Submit ➝ Pending ➝ Started ➝ Success or Failure ➝ Notify