# About Book Review API

A lightweight book review API built with **FastAPI**, designed to practice nested models, relationship handling, full CRUD operations, and schema-driven validation. Books can have **multiple reviews**, and the API supports **filtering**, **pagination**, and a review **summary endpoint** for quick insights.

---

# Route Documentation

This API allows you to create, retrieve, update, delete, and review books. It supports nested data structures and flexible filtering by query parameters.

---

## `GET /books/`

**Description:** Retrieve all books with optional filtering and pagination.

**Query Parameters:**

| Name     | Type                 | Description                               |
| -------- | -------------------- | ----------------------------------------- |
| `author` | `str` (optional)     | Filter by exact author (case-insensitive) |
| `genre`  | `str` (optional)     | Filter by genre (case-insensitive)        |
| `limit`  | `int` (default=`10`) | Max number of books to return             |
| `skip`   | `int` (default=`0`)  | Number of books to skip (for pagination)  |

**Response:** `200 OK`
Returns a list of books.

---

## `GET /books/{book_id}`

**Description:** Retrieve a single book by its ID, including all associated reviews.

**Path Parameter:**

| Name      | Type   | Description          |
| --------- | ------ | -------------------- |
| `book_id` | `UUID` | The book's unique ID |

**Response:** `200 OK`
Returns the full book data with a `reviews` list.
**Error:** `404 Not Found` if the book does not exist.

---

## `POST /books/`

**Description:** Create a new book entry.

**Request Body:** (Uses `BookCreate` schema)

```json
{
  "title": "The Pragmatic Programmer",
  "author": "Andrew Hunt",
  "genre": "Technology",
  "published_year": 1999
}
```

**Response:** `201 Created`
Returns the created book with a UUID.

---

## `PUT /books/{book_id}`

**Description:** Update an existing book.

**Path Parameter:**

| Name      | Type   | Description          |
| --------- | ------ | -------------------- |
| `book_id` | `UUID` | The book's unique ID |

**Request Body:** (Uses `BookUpdate` schema)

```json
{
  "title": "Updated Title",
  "author": "New Author",
  "genre": "Updated Genre",
  "published_year": 2024
}
```

**Response:** `200 OK`
Returns the updated book.
**Error:** `404 Not Found` if the book does not exist.

---

## `DELETE /books/{book_id}`

**Description:** Delete a book and all its reviews.

**Path Parameter:**

| Name      | Type   | Description          |
| --------- | ------ | -------------------- |
| `book_id` | `UUID` | The book's unique ID |

**Response:** `204 No Content`
Book and associated reviews are removed.
**Error:** `404 Not Found` if the book does not exist.

---

## `GET /books/{book_id}/reviews/`

**Description:** Retrieve all reviews for a given book, with optional filters and pagination.

**Query Parameters:**

| Name         | Type                 | Description                           |
| ------------ | -------------------- | ------------------------------------- |
| `rating`     | `int` (optional)     | Filter by exact rating                |
| `min_rating` | `int` (optional)     | Filter by minimum rating              |
| `reviewer`   | `str` (optional)     | Filter by reviewer (case-insensitive) |
| `limit`      | `int` (default=`10`) | Max number of reviews to return       |
| `skip`       | `int` (default=`0`)  | Number of reviews to skip             |

**Response:** `200 OK`
Returns list of reviews for the book.
**Error:** `404 Not Found` if the book does not exist.

---

## `POST /books/{book_id}/reviews/`

**Description:** Add a new review for a specific book.

**Request Body:** (Uses `ReviewCreate` schema)

```json
{
  "reviewer": "Alice",
  "rating": 5,
  "text": "An excellent and practical book."
}
```

**Response:** `201 Created`
Returns the created review with `id`, `book_id`, and `created_at`.

---

## `GET /books/{book_id}/review-summary`

**Description:** Retrieve a summary of reviews for a specific book.

**Response Body:**

```json
{
  "book_id": "uuid",
  "average_rating": 4.5,
  "total_reviews": 3
}
```

**Response:** `200 OK`
Provides quick insight into overall book ratings.
**Error:** `404 Not Found` if the book does not exist.

---

## Notes

* All books and reviews include a unique `id` and appropriate timestamps.
* Data is stored in **in-memory lists** (`books_db`, `reviews_db`) — no external DB used.
* The API was built as a **learning project** to explore FastAPI, Pydantic, and nested routing.