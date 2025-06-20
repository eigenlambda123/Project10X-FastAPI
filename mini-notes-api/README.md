# About Mini Notes API

A lightweight note-taking API built with **FastAPI**, designed for practicing full CRUD operations, in-memory data handling, and schema-driven validation. Notes support **Markdown content**, optional **tags**, and dynamic querying via search and pagination.

---

# Route Documentation

This API allows you to create, retrieve, update, delete, and search notes. Responses include Markdown-rendered content and support filtering and pagination for flexibility.

---

## `GET /notes`

**Description:** Retrieve all notes with optional search, tag filtering, and pagination.

**Query Parameters:**

| Name     | Type                 | Description                              |
| -------- | -------------------- | ---------------------------------------- |
| `search` | `str` (optional)     | Filter by text in title or content       |
| `tag`    | `str` (optional)     | Filter by tag (case-insensitive)         |
| `limit`  | `int` (default=`10`) | Max number of notes to return            |
| `skip`   | `int` (default=`0`)  | Number of notes to skip (for pagination) |

**Response:** `200 OK`
Returns a list of notes with Markdown-rendered content in the `content` field.

---

## `GET /notes/{note_id}`

**Description:** Retrieve a single note by its ID.

**Path Parameter:**

| Name      | Type   | Description          |
| --------- | ------ | -------------------- |
| `note_id` | `UUID` | The note's unique ID |

**Response:** `200 OK`
Returns the full note data.
**Error:** `404 Not Found` if the note does not exist.

---

## `POST /notes`

**Description:** Create a new note.

**Request Body:** (Uses `NoteCreate` schema)

```json
{
  "title": "Meeting notes",
  "content": "Discuss project updates",
  "tags": ["work", "personal"]
}
```

**Response:** `201 Created`
Returns the created note with a UUID and timestamp. Markdown is rendered into HTML in the `content` field.

---

## `PUT /notes/{note_id}`

**Description:** Update an existing note by ID.

**Path Parameter:**

| Name      | Type   | Description          |
| --------- | ------ | -------------------- |
| `note_id` | `UUID` | The note's unique ID |

**Request Body:** (Partial update using `NoteUpdate` schema)

```json
{
  "title": "Updated title",
  "tags": ["final", "review"]
}
```

**Response:** `200 OK`
Returns the updated note.
**Error:** `404 Not Found` if the note does not exist.

---

## `DELETE /notes/{note_id}`

**Description:** Delete a note by ID.

**Path Parameter:**

| Name      | Type   | Description          |
| --------- | ------ | -------------------- |
| `note_id` | `UUID` | The note's unique ID |

**Response:** `200 OK`
Returns the deleted note.
**Error:** `404 Not Found` if the note does not exist.

---

## Notes

* All notes include a unique `id`, `created_at` timestamp, and optional `tags`.
* `content` is automatically converted from Markdown to HTML before being returned.
* Data is stored in an **in-memory list** (`notes_db`) — no external database is used.
* Built for practice, learning, and rapid prototyping with FastAPI.