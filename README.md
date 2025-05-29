# Forum API

An asynchronous REST API built with FastAPI for managing a forum with topics, posts, and comments.

## Overview

- **FastAPI** with asynchronous SQLAlchemy (AsyncSession)
- Full CRUD operations for topics, posts, and comments
- Pagination and sorting support
- Proper error handling with HTTP status codes
- Auto-generated Swagger UI documentation (`/docs`)

---

## Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt` (FastAPI, SQLAlchemy, asyncpg or aiosqlite, etc.)

---

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_folder>
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Service

Start the API server with hot reload:

```bash
uvicorn app.main:app --reload
```

- API available at: http://localhost:8000
- Swagger UI docs: http://localhost:8000/docs
- ReDoc docs: http://localhost:8000/redoc

## API Endpoints

### Topics (/topics)

- `POST /topics/` — Create a new topic
- `GET /topics/` — List topics (supports pagination with `skip` and `limit`)
- `GET /topics/{topic_id}` — Retrieve a topic by ID
- `PUT /topics/{topic_id}` — Update a topic
- `DELETE /topics/{topic_id}` — Delete a topic (only if no posts exist)
- `POST /topics/{topic_id}/posts` — Create a post under a specific topic

### Posts (/posts)

- `POST /posts/` — Create a new post
- `GET /posts/` — List posts (supports pagination and sorting by `sort_by` and `order`)
- `GET /posts/{post_id}` — Retrieve a post by ID
- `PUT /posts/{post_id}` — Update a post
- `DELETE /posts/{post_id}` — Delete a post

### Comments (/comments)

- `POST /comments/post/{post_id}` — Create a comment for a specific post
- `GET /comments/post/{post_id}` — List comments for a post (supports pagination and sorting)
- `GET /comments/{comment_id}` — Retrieve a comment by ID
- `PUT /comments/{comment_id}` — Update a comment
- `DELETE /comments/{comment_id}` — Delete a comment
