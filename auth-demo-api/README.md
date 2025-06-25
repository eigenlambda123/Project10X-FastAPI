# About Auth Demo API

A minimal but secure authentication API built with **FastAPI**, designed to practice manual JWT handling, password hashing, user login and registration, and **role-based access control** (RBAC). This project highlights the internals of authentication flow using `OAuth2PasswordBearer`, `passlib`, and `python-jose`.

---

# Route Documentation

This API provides secure user authentication using **Bearer JWT tokens**, with support for login, registration, current user info, and admin-only access.

---

## `POST /auth/register`

**Description:** Register a new user.

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "secure123",
  "role": "user"
}
```

**Validation Rules:**

* `email`: must be valid format
* `password`: minimum length of 6 characters
* `role`: must be `"user"` or `"admin"`

**Response:** `201 Created`
Returns the created user without password.

---

## `POST /auth/login`

**Description:** Authenticates a user and returns a JWT access token.

**Form Fields:** (sent as `application/x-www-form-urlencoded`)

* `username`: string
* `password`: string

**Response:** `200 OK`

```json
{
  "access_token": "JWT_TOKEN_STRING",
  "token_type": "bearer"
}
```

Use this token to access protected routes by setting:

```
Authorization: Bearer JWT_TOKEN_STRING
```

---

## `GET /auth/me`

**Description:** Returns the authenticated user's information.

**Authentication Required:** ✅ Yes
Use `Bearer` token from `/auth/login`

**Response:** `200 OK`

```json
{
  "id": "uuid",
  "username": "johndoe",
  "email": "johndoe@example.com",
  "is_active": true,
  "role": "user"
}
```

**Error:** `401 Unauthorized` if token is missing or invalid.

---

## `GET /auth/admin`

**Description:** Admin-only route that returns current admin user info.

**Authentication Required:** ✅ Yes
**Authorization Required:** Must have `role: "admin"`

**Response:** `200 OK` — same as `/auth/me`

**Error:**

* `401 Unauthorized` if no valid token
* `403 Forbidden` if user is not an admin

---

# Data Handling

* Users are stored in an **in-memory dictionary** `fake_users_db` with hashed passwords.
* User `id` values are generated using `uuid4()`.
* Passwords are hashed using **bcrypt** via `passlib`.
* JWTs are signed using **HS256** with `python-jose`, and include:

  * `sub` (username)
  * `exp` (expiration)
  * `role` (user/admin)

---

# Roles & Permissions

| Role  | Description                          |
| ----- | ------------------------------------ |
| user  | Can login and view own data          |
| admin | Can access protected `/admin` routes |

Role checking is enforced using FastAPI **dependencies** like `get_current_user` and `get_current_admin`.

---

# Notes

* Token-based auth flow is handled manually for learning purposes.
* The app is a **stateless** API — no session cookies.
* Used only for understanding how JWT auth, hashing, and role control work without using a full database or third-party auth package.