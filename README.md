# Role base permission fastAPI

FastAPI example project with:

- JWT authentication
- role-based authorization
- SQLite persistence
- SQLAlchemy ORM
- seeded dummy users
- post and comment ownership rules

## What This Covers

- `Super Admin`: can delete any post or comment
- `Moderator`: can delete any post or comment, but cannot manage users
- `Regular User`: can create posts and comments, and can update or delete only their own posts
- `Guest`: can only read

Post rules:

- regular users can create posts
- a user can update only their own post
- a user can delete only their own post
- moderators and super admins can delete any post

Comment rules:

- User B can comment on User A's post
- User A can delete User B's comment on User A's post
- User B can delete their own comment
- User C cannot delete User B's comment
- moderators and super admins can delete any comment

## Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy
- SQLite
- custom JWT handling

## Project Structure

```text
app/
|-- api/v1/
|   |-- auth.py
|   |-- comments.py
|   `-- posts.py
|-- core/
|   |-- config.py
|   |-- logger.py
|   `-- security.py
|-- database/
|   |-- base.py
|   |-- connection.py
|   `-- entities.py
|-- exceptions/
|   `-- custom_exception.py
|-- models/
|   |-- comment.py
|   |-- post.py
|   `-- user.py
|-- repositories/
|   |-- comment_repository.py
|   |-- post_repository.py
|   `-- user_repository.py
|-- schemas/
|   |-- auth.py
|   |-- comment.py
|   `-- post.py
|-- services/
|   |-- auth_service.py
|   |-- authorization_service.py
|   |-- comment_service.py
|   `-- post_service.py
|-- dependencies.py
`-- main.py
tests/
|-- test_api.py
`-- test_auth.py
.env.example
migrate.py
seed.py
requirements.txt
README.md
```

## Setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Create `.env`

Create a local `.env` file from `.env.example`.

Example:

```env
APP_NAME=Posts API
API_PREFIX=/api/v1
DATABASE_URL=sqlite:///./app.db
JWT_SECRET=change-me
```

Environment values:

- `APP_NAME`: application name used for local configuration
- `API_PREFIX`: API route prefix
- `DATABASE_URL`: database connection string
- `JWT_SECRET`: secret used to sign access tokens

### 4. Initialize the database

This project uses a local SQLite database file named `app.db`.

Run:

```powershell
python seed.py
python migrate.py
```

Notes:

- `seed.py` resets local DB contents to the seeded state
- `migrate.py` creates the schema if it does not exist
- `app.db` is ignored by git

### 5. Run the API

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000/docs`

## Seeded Users

- `admin@example.com` / `admin123` -> `super_admin`
- `moderator@example.com` / `moderator123` -> `moderator`
- `usera@example.com` / `usera123` -> `regular_user`
- `userb@example.com` / `userb123` -> `regular_user`
- `userc@example.com` / `userc123` -> `regular_user`
- `guest@example.com` / `guest123` -> `guest`

Seeded content:

- one initial post owned by `usera@example.com`

## Authentication

Login endpoint:

- `POST /api/v1/auth/login`

Request body:

```json
{
  "email": "usera@example.com",
  "password": "usera123"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Use the token in requests:

```http
Authorization: Bearer <jwt>
```

## API Endpoints

- `POST /api/v1/auth/login`
- `GET /api/v1/posts`
- `GET /api/v1/posts/{post_id}`
- `POST /api/v1/posts`
- `PUT /api/v1/posts/{post_id}`
- `DELETE /api/v1/posts/{post_id}`
- `GET /api/v1/posts/{post_id}/comments`
- `POST /api/v1/posts/{post_id}/comments`
- `DELETE /api/v1/posts/{post_id}/comments/{comment_id}`

## Testing

Run:

```powershell
python -m unittest discover -s tests -v
```

Covered by tests:

- role definitions
- login failure handling
- guest read access
- regular user post ownership rules
- comment ownership rules
- moderator delete-any behavior
- super admin delete-any behavior
