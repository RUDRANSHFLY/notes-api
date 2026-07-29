# Notes API (Python)

A REST API for a notes-taking application built with **FastAPI**. Supports full CRUD operations on notes with unique title enforcement, layered architecture, and Swagger/OpenAPI documentation.

> Built with **Cursor Composer 2.5 Fast** (Normal plan).

---

## Tech Stack

| Tool / Library | Purpose |
|----------------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) (`fastapi[standard]`) | Web framework, validation, auto-generated OpenAPI docs |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server (included with `fastapi[standard]`) |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM for database models and queries |
| [Pydantic](https://docs.pydantic.dev/) | Request/response DTO validation (via FastAPI) |
| [uv](https://docs.astral.sh/uv/) | Python package manager and virtual environment |
| **SQLite** | File-based database stored in `db/notes.db` |

**Python version:** `>=3.14`

---

## Folder Structure

```
notes-api-python/
├── app/
│   ├── app.py                          # FastAPI app entry point (title, description, tags)
│   ├── __init__.py
│   └── notes/
│       ├── __init__.py                 # Re-exports models, dto, service, controllers
│       ├── models/
│       │   ├── __init__.py
│       │   └── note.py                 # SQLAlchemy Note model (id, title, content)
│       ├── dto/
│       │   ├── __init__.py
│       │   └── note_dto.py             # Pydantic DTOs with Swagger field metadata
│       ├── service/
│       │   ├── __init__.py
│       │   └── note_service.py         # Business logic, unique title checks
│       └── controllers/
│           ├── __init__.py
│           └── note_controller.py      # API routes with summary, description, responses
├── db/
│   ├── __init__.py
│   ├── database.py                     # SQLite engine, session, init_db()
│   └── notes.db                        # SQLite database file (auto-created on first run)
├── pyproject.toml                      # Project metadata and dependencies
├── uv.lock                             # Locked dependency versions
└── README.md
```

### Layer responsibilities

| Layer | Location | Role |
|-------|----------|------|
| **Controllers** | `app/notes/controllers/` | HTTP routes, status codes, request/response handling |
| **Service** | `app/notes/service/` | Business rules (unique title, not-found checks) |
| **DTO** | `app/notes/dto/` | Pydantic schemas for create, update, and response payloads |
| **Models** | `app/notes/models/` | SQLAlchemy database table definitions |
| **Database** | `db/` | Connection setup, session management, table creation |

Every sub-package exposes its public API through `__init__.py` via `__all__`.

---

## Database

- **Engine:** SQLite
- **File:** `db/notes.db` (created automatically on startup)
- **Table:** `notes`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `title` | String | **Unique**, not null, indexed |
| `content` | String | Not null |

Title uniqueness is enforced at both the **service layer** (returns `409 Conflict`) and the **database layer** (`unique=True` on the column).

---

## API Endpoints

Base URL: `http://127.0.0.1:8000`

| Method | Path | Summary | Success | Error codes |
|--------|------|---------|---------|-------------|
| `POST` | `/notes` | Create a note | `201` | `409` duplicate title, `422` validation |
| `GET` | `/notes` | Get all notes | `200` | — |
| `GET` | `/notes/{note_id}` | Get note by ID | `200` | `404` not found |
| `PUT` | `/notes/{note_id}` | Update a note | `200` | `404`, `409`, `400`, `422` |
| `DELETE` | `/notes/{note_id}` | Delete a note | `200` | `404` not found |

### Response format

All endpoints return a consistent JSON shape:

```json
{
  "message": "Human-readable status message",
  "data": { "id": 1, "title": "...", "content": "..." }
}
```

On error, `data` is `null` and `message` describes the failure.

### Swagger / OpenAPI docs

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/docs | Swagger UI (interactive) |
| http://127.0.0.1:8000/redoc | ReDoc (read-only) |

---

## Getting Started

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Install dependencies

```powershell
cd D:\ai\notes-api-python
python -m uv sync
```

Or add packages manually (as used during initial setup):

```powershell
python -m uv add "fastapi[standard]" sqlalchemy
```

### Run the server

```powershell
python -m uv run uvicorn app.app:app --reload
```

Server runs at **http://127.0.0.1:8000**.

### Example requests

```powershell
# Create a note
curl -X POST http://127.0.0.1:8000/notes `
  -H "Content-Type: application/json" `
  -d '{"title":"My Note","content":"Note body"}'

# Get all notes
curl http://127.0.0.1:8000/notes

# Get one note
curl http://127.0.0.1:8000/notes/1

# Update a note
curl -X PUT http://127.0.0.1:8000/notes/1 `
  -H "Content-Type: application/json" `
  -d '{"title":"Updated","content":"New content"}'

# Delete a note
curl -X DELETE http://127.0.0.1:8000/notes/1
```

---

## Build Timeline & Prompts

This project was built iteratively through **Cursor** on **Wednesday, July 29, 2026** (timezone: **UTC+5:30 / IST**).

**AI assistant:** Cursor Composer 2.5 Fast · Normal plan

| # | Time (IST) | Prompt | What was built |
|---|------------|--------|----------------|
| **1** | **7:20 AM** | *"Create a API for the notes taking app… make with FastAPI and uv package manager `uv add fastapi[standard]`… notes model with title and content (both strings)… CRUD operations… new db folder… inside app there should be app.py and notes folder with separation of models, controllers, service, and dto… all exports in module `__init__.py`… proper status codes and messages… at create time check same title doesn't get inserted, should be unique always… same checks for find all, update, and delete."* | Initialized uv project, added `fastapi[standard]` + SQLAlchemy, created layered folder structure (`app/`, `db/`, models/dto/service/controllers), implemented full CRUD with unique title validation, consistent `{ message, data }` responses, and endpoint testing |
| **2** | **7:50 AM** | *"Add swagger docs for each controller and add title, description, and DTO/app API property for that."* | Added OpenAPI metadata on `FastAPI` app (title, description, tags, contact, license), per-endpoint `summary`/`description`/`responses` on all controllers, and `Field` titles/descriptions/examples on all DTOs |
| **3** | **7:58 AM** | *"Update README.md — whatever we used like FastAPI and folder structure and also DB… add what prompts I have given and its timeline… give exact timings for each prompt."* | This README |

### Build milestones (from session logs)

| Milestone | Completed at (IST) |
|-----------|-------------------|
| uv project initialized | 7:24:57 AM |
| Dependencies installed (`fastapi[standard]`, SQLAlchemy) | ~7:26 AM |
| Server started, CRUD tests passed | 7:28:30 AM |
| Swagger/OpenAPI docs added | ~7:52 AM |
| README written | 7:58 AM |

---

## Author

**RUDRANSH BARADIYA** — mayamayavir@gmail.com
# notes-api
