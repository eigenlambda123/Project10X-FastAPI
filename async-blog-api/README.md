# About Async Blog API

A clean, async-ready blog backend built with **FastAPI** and **SQLModel**, supporting **tag-based filtering**, **pagination**, **nested comments**, and **admin-only moderation** via JWT. This project showcases best practices in API design with SQLModel, including relational modeling, query optimization, and modular route structure.

---

## Route Documentation

The API enables users to manage blog posts and tags, filter by tag, paginate results, and interact through comments. It also supports admin-restricted moderation features.

---

### **POST /posts/**

**Description:** Create a new blog post. Optionally include tag IDs to associate.

**Request Body:**

```json
{
  "title": "My Post",
  "content": "This is a blog post.",
  "tag_ids": [1, 2]
}
```

**Response:**

Returns the created post, including associated tags.

---

### **GET /posts/**

**Description:** List blog posts, with optional filtering and pagination.

**Query Parameters:**

| Name   | Type   | Default | Description                              |
| ------ | ------ | ------- | ---------------------------------------- |
| tag    | string | `null`  | Filter by tag name                       |
| limit  | int    | `10`    | Max number of posts to return (max: 100) |
| offset | int    | `0`     | Number of posts to skip                  |

**Response:**

```json
{
  "total": 25,
  "limit": 10,
  "offset": 0,
  "items": [
    {
      "id": 1,
      "title": "Hello World",
      "content": "...",
      "tags": [...]
    }
  ]
}
```

---

### **GET /posts/{id}**

**Description:** Retrieve a single blog post by ID. Includes nested comments.

**Response:**

```json
{
  "id": 1,
  "title": "Post Title",
  "content": "...",
  "tags": [...],
  "comments": [
    {
      "id": 1,
      "content": "Nice post!",
      "created_at": "2025-07-07T12:00:00"
    }
  ]
}
```

---

### **PUT /posts/{id}**

**Description:** Update a blog post and its tags.

**Request Body:** Same as `POST /posts/`

---

### **DELETE /posts/{id}**

**Description:** Delete a blog post by ID.

---

### **GET /tags/**

**Description:** List all tags.

---

### **POST /tags/**

**Description:** Create a new tag.

---

### **GET /posts/{id}/comments/**

**Description:** Get comments associated with a post.

---

### **POST /posts/{id}/comments/**

**Description:** Add a new comment to a post.

**Request Body:**

```json
{
  "content": "This is a comment."
}
```

---

### **DELETE /posts/{post\_id}/comments/{id}**

**Description:** Admin-only endpoint to delete a comment.

**Header:**

`Authorization: Bearer <admin_jwt_token>`

---

## Features

| Feature                  | Description                                                           |
| ------------------------ | --------------------------------------------------------------------- |
| **Async SQLModel**       | Models and queries using `AsyncSession` and `sqlmodel.ext.asyncio`    |
| **Many-to-Many Tags**    | Implemented using link tables and `relationship(..., back_populates)` |
| **Tag Filtering**        | Query posts by tag name using `.join()` and `.where()` logic          |
| **Pagination**           | Custom pagination with `limit`, `offset`, and total count metadata    |
| **Nested Comments**      | Comments returned under `/posts/{id}` via eager loading               |
| **JWT-Based Admin Auth** | Role-based endpoint protection using token claims                     |

---

## Models

* `BlogPost`: Title, content, timestamps, tags, comments
* `Tag`: Name (many-to-many with `BlogPost`)
* `Comment`: Foreign key to post, content, created\_at
* `User`: Email, hashed password, is\_admin (used for JWT)
* Pydantic models: `BlogPostCreate`, `BlogPostRead`, `BlogPostReadNoComments`, etc.

---

## Project Structure

```
async-blog-api/
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── posts.py
│   │   ├── tags.py
│   │   └── comments.py
│   ├── utils/
│   │   └── pagination.py (optional)
│   └── core/
│       └── auth.py
└── requirements.txt
```

---

## Auth Setup

* Tokens are signed using `pyjwt` and contain `sub` (email) and `is_admin` boolean.
* Use `/token` endpoint (from Project 4 or your own) to obtain a token.
* Protect admin routes using `Depends(get_current_admin_user)`.

---

## Notes

* Pydantic V2 `model_validate()` is used for converting ORM models.
* `selectinload()` avoids N+1 problems when joining related models.
* To avoid circular data (like nested comments inside `read_posts/`), a separate schema (`BlogPostReadNoComments`) is used.
