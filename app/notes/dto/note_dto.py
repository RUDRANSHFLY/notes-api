from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class NoteCreateDTO(BaseModel):
    """Request body for creating a new note."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Meeting Notes",
                    "content": "Discuss project roadmap and deadlines.",
                }
            ]
        }
    )

    title: str = Field(
        ...,
        min_length=1,
        title="Title",
        description="Unique title of the note. Must not duplicate an existing note title.",
        examples=["Meeting Notes"],
    )
    content: str = Field(
        ...,
        min_length=1,
        title="Content",
        description="Body text of the note.",
        examples=["Discuss project roadmap and deadlines."],
    )


class NoteUpdateDTO(BaseModel):
    """Request body for updating an existing note. At least one field is required."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "title": "Updated Meeting Notes",
                    "content": "Revised agenda and action items.",
                }
            ]
        }
    )

    title: str | None = Field(
        default=None,
        min_length=1,
        title="Title",
        description="New title for the note. Must remain unique across all notes.",
        examples=["Updated Meeting Notes"],
    )
    content: str | None = Field(
        default=None,
        min_length=1,
        title="Content",
        description="New body text for the note.",
        examples=["Revised agenda and action items."],
    )


class NoteResponseDTO(BaseModel):
    """Note data returned by the API."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "title": "Meeting Notes",
                    "content": "Discuss project roadmap and deadlines.",
                }
            ]
        },
    )

    id: int = Field(
        ...,
        title="ID",
        description="Unique identifier of the note.",
        examples=[1],
    )
    title: str = Field(
        ...,
        title="Title",
        description="Unique title of the note.",
        examples=["Meeting Notes"],
    )
    content: str = Field(
        ...,
        title="Content",
        description="Body text of the note.",
        examples=["Discuss project roadmap and deadlines."],
    )


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper with a message and optional data payload."""

    message: str = Field(
        ...,
        title="Message",
        description="Human-readable status message describing the result of the operation.",
        examples=["Note created successfully"],
    )
    data: T | None = Field(
        default=None,
        title="Data",
        description="Response payload. Returns `null` when no data is available or on error.",
    )
