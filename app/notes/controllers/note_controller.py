from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.notes.dto import ApiResponse, NoteCreateDTO, NoteResponseDTO, NoteUpdateDTO
from app.notes.service import DuplicateTitleError, NoteNotFoundError, NoteService
from db.database import get_db

router = APIRouter(prefix="/notes", tags=["Notes"])


def get_note_service(db: Session = Depends(get_db)) -> NoteService:
    return NoteService(db)


@router.post(
    "",
    summary="Create a note",
    description=(
        "Creates a new note with a **title** and **content**. "
        "The title must be unique — if a note with the same title already exists, "
        "the request is rejected with `409 Conflict`."
    ),
    response_model=ApiResponse[NoteResponseDTO],
    response_description="Note created successfully.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "A note with the same title already exists.",
            "model": ApiResponse[None],
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Validation error — title or content is missing or empty.",
        },
    },
)
def create_note(
    payload: NoteCreateDTO,
    service: NoteService = Depends(get_note_service),
):
    try:
        note = service.create(payload)
        return ApiResponse(message="Note created successfully", data=note)
    except DuplicateTitleError as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(exc), "data": None},
        )


@router.get(
    "",
    summary="Get all notes",
    description=(
        "Retrieves every note stored in the database, ordered by ID. "
        "Returns an empty list with message `No notes found` when no notes exist."
    ),
    response_model=ApiResponse[list[NoteResponseDTO]],
    response_description="List of all notes.",
)
def get_all_notes(service: NoteService = Depends(get_note_service)):
    notes = service.get_all()
    if not notes:
        return ApiResponse(message="No notes found", data=[])
    return ApiResponse(message="Notes retrieved successfully", data=notes)


@router.get(
    "/{note_id}",
    summary="Get a note by ID",
    description="Retrieves a single note by its unique numeric identifier.",
    response_model=ApiResponse[NoteResponseDTO],
    response_description="Note retrieved successfully.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No note exists with the given ID.",
            "model": ApiResponse[None],
        },
    },
)
def get_note(
    note_id: int = Path(
        ...,
        title="Note ID",
        description="Unique numeric identifier of the note to retrieve.",
        ge=1,
        examples=[1],
    ),
    service: NoteService = Depends(get_note_service),
):
    try:
        note = service.get_by_id(note_id)
        return ApiResponse(message="Note retrieved successfully", data=note)
    except NoteNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc), "data": None},
        )


@router.put(
    "/{note_id}",
    summary="Update a note",
    description=(
        "Updates an existing note by ID. Provide **title**, **content**, or both. "
        "At least one field is required. If the new title conflicts with another note, "
        "the request is rejected with `409 Conflict`."
    ),
    response_model=ApiResponse[NoteResponseDTO],
    response_description="Note updated successfully.",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Neither title nor content was provided in the request body.",
            "model": ApiResponse[None],
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No note exists with the given ID.",
            "model": ApiResponse[None],
        },
        status.HTTP_409_CONFLICT: {
            "description": "The requested title is already used by another note.",
            "model": ApiResponse[None],
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Validation error — provided title or content is empty.",
        },
    },
)
def update_note(
    note_id: int = Path(
        ...,
        title="Note ID",
        description="Unique numeric identifier of the note to update.",
        ge=1,
        examples=[1],
    ),
    payload: NoteUpdateDTO = ...,
    service: NoteService = Depends(get_note_service),
):
    try:
        note = service.update(note_id, payload)
        return ApiResponse(message="Note updated successfully", data=note)
    except NoteNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc), "data": None},
        )
    except DuplicateTitleError as exc:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(exc), "data": None},
        )
    except ValueError as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc), "data": None},
        )


@router.delete(
    "/{note_id}",
    summary="Delete a note",
    description="Permanently deletes a note by its unique numeric identifier.",
    response_model=ApiResponse[None],
    response_description="Note deleted successfully.",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No note exists with the given ID.",
            "model": ApiResponse[None],
        },
    },
)
def delete_note(
    note_id: int = Path(
        ...,
        title="Note ID",
        description="Unique numeric identifier of the note to delete.",
        ge=1,
        examples=[1],
    ),
    service: NoteService = Depends(get_note_service),
):
    try:
        service.delete(note_id)
        return ApiResponse(message="Note deleted successfully", data=None)
    except NoteNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc), "data": None},
        )
