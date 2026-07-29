from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.notes.controllers import router as notes_router
from db.database import init_db

OPENAPI_TAGS = [
    {
        "name": "Notes",
        "description": (
            "CRUD operations for managing notes. "
            "Each note has a unique **title** and a **content** body. "
            "All responses follow the `{ message, data }` format."
        ),
    },
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Notes API",
    description="""
REST API for a notes taking application.

## Overview
Manage notes with full CRUD support. Every note requires a **title** and **content**, both stored as strings.

## Rules
- **Unique titles** — duplicate titles are rejected on create and update (`409 Conflict`).
- **Consistent responses** — every endpoint returns `{ "message": "...", "data": ... }`.
- **Validation** — empty title or content is rejected with `422 Unprocessable Content`.

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/notes` | Create a new note |
| `GET` | `/notes` | List all notes |
| `GET` | `/notes/{note_id}` | Get a note by ID |
| `PUT` | `/notes/{note_id}` | Update a note |
| `DELETE` | `/notes/{note_id}` | Delete a note |
    """,
    version="1.0.0",
    contact={
        "name": "Notes API",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=OPENAPI_TAGS,
    lifespan=lifespan,
)

app.include_router(notes_router)
