from sqlalchemy.orm import Session

from app.notes.dto import NoteCreateDTO, NoteResponseDTO, NoteUpdateDTO
from app.notes.models import Note


class NoteNotFoundError(Exception):
    pass


class DuplicateTitleError(Exception):
    pass


class NoteService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def _get_by_title(self, title: str) -> Note | None:
        return self._db.query(Note).filter(Note.title == title).first()

    def _get_by_id(self, note_id: int) -> Note | None:
        return self._db.query(Note).filter(Note.id == note_id).first()

    def create(self, payload: NoteCreateDTO) -> NoteResponseDTO:
        if self._get_by_title(payload.title):
            raise DuplicateTitleError(f"A note with title '{payload.title}' already exists")

        note = Note(title=payload.title, content=payload.content)
        self._db.add(note)
        self._db.commit()
        self._db.refresh(note)
        return NoteResponseDTO.model_validate(note)

    def get_all(self) -> list[NoteResponseDTO]:
        notes = self._db.query(Note).order_by(Note.id).all()
        return [NoteResponseDTO.model_validate(note) for note in notes]

    def get_by_id(self, note_id: int) -> NoteResponseDTO:
        note = self._get_by_id(note_id)
        if not note:
            raise NoteNotFoundError(f"Note with id {note_id} not found")
        return NoteResponseDTO.model_validate(note)

    def update(self, note_id: int, payload: NoteUpdateDTO) -> NoteResponseDTO:
        note = self._get_by_id(note_id)
        if not note:
            raise NoteNotFoundError(f"Note with id {note_id} not found")

        if payload.title is None and payload.content is None:
            raise ValueError("At least one of title or content must be provided")

        if payload.title is not None and payload.title != note.title:
            if self._get_by_title(payload.title):
                raise DuplicateTitleError(f"A note with title '{payload.title}' already exists")
            note.title = payload.title

        if payload.content is not None:
            note.content = payload.content

        self._db.commit()
        self._db.refresh(note)
        return NoteResponseDTO.model_validate(note)

    def delete(self, note_id: int) -> None:
        note = self._get_by_id(note_id)
        if not note:
            raise NoteNotFoundError(f"Note with id {note_id} not found")
        self._db.delete(note)
        self._db.commit()
