# About Background Tasks Service

A minimal asynchronous task service built with **FastAPI**, designed to simulate how backend systems handle background work like sending notifications, generating reports, and writing files — **after** returning the response to the client. It showcases FastAPI’s `BackgroundTasks`, custom task tracking, retry logic, and simulated async file generation using Python’s standard library.

---

## Route Documentation

This API allows you to **trigger background jobs**, **track task progress**, and optionally **retry failed tasks**. All tasks are simulated and tracked in-memory using a task registry.

---

### **POST /notify/**

**Description:** Triggers a background task to simulate sending an email notification.

**Request Body:**

```json
{
  "email": "johndoe@example.com",
  "message": "Your submission was received."
}
```

**Response: 202 Accepted**

```json
{
  "task_id": "uuid",
  "status": "started"
}
```

---

### **POST /report/**

**Description:** Triggers a background task to simulate generating a report.

**Request Body:**

```json
{
  "name": "Sales Report",
  "details": {
    "month": "June",
    "region": "Asia"
  }
}
```

**Response: 202 Accepted**

```json
{
  "task_id": "uuid",
  "status": "started"
}
```

---

### **POST /file/**

**Description:** Triggers an async task to generate and save a `.json` file from provided content.

**Request Body:**

```json
{
  "content": {
    "user": "johndoe",
    "activity": "export"
  }
}
```

**Response: 202 Accepted**

```json
{
  "task_id": "uuid",
  "status": "started"
}
```

---

### **GET /status/{task\_id}**

**Description:** Returns the status of a task, including result or error message if applicable.

**Response: 200 OK**

```json
{
  "id": "uuid",
  "type": "report",
  "status": "success",
  "result": {
    "message": "Report generated"
  },
  "error": null,
  "timestamp": "2025-06-26T..."
}
```

**Error:**

* `404 Not Found` if task ID does not exist

---

### **POST /retry-task/{task\_id}**

**Description:** Manually re-triggers a previously failed task.

**Response: 200 OK**

```json
{
  "task_id": "uuid",
  "status": "retried"
}
```

**Error:**

* `400 Bad Request` if task is not in a "failed" state
* `404 Not Found` if task ID is invalid or missing

---

## Task Handling

Tasks are stored in an in-memory `task_store` dictionary. Each task contains:

| Field       | Description                                    |
| ----------- | ---------------------------------------------- |
| `id`        | UUID of the task                               |
| `type`      | Task type: `notification`, `report`, or `file` |
| `status`    | `pending`, `success`, `failed`                 |
| `result`    | Result data if successful                      |
| `error`     | Error message if failed                        |
| `timestamp` | When the task was triggered                    |
| `retries`   | How many times the task was retried            |

---

## Task Types

| Task         | Description                              | Simulated Delay | Notes                         |
| ------------ | ---------------------------------------- | --------------- | ----------------------------- |
| Notification | Mimics sending a confirmation email      | \~2 seconds     | Returns success/failure       |
| Report       | Mimics generating a backend report       | \~3 seconds     | Returns a dummy report result |
| File         | Creates a `.json` file in `outputs/` dir | \~2 seconds     | Saves structured data to disk |

---

## Retry & Error Handling

* All background functions are wrapped in `try/except` blocks
* On failure, the error is logged in the task metadata
* Failed tasks can be **manually retried** via `/retry-task/{task_id}`
* Retry count is tracked in the `task_store`

---

## Notes

* No external queue like Celery or Redis is used — everything is in-memory for simulation.
* File generation is synchronous but triggered through `BackgroundTasks` for realism.
* Task IDs are generated via `uuid4()` and used to reference status.