from fastapi import APIRouter, HTTPException
from app.schemas import Note
from app.models import notes_db
from uuid import UUID

router = APIRouter()

@router.get("/notes", response_model=list[Note]) # endpoint to retrieve all notes
def get_notes():
    """
    Retrieve all notes
    """
    return notes_db


@router.post("/notes", response_model=Note) # endpoint to create a new note
def create_note(note: Note):
    """
    Create a new note
    """
    new_note = Note(**note.dict()) # auto generate id and created_at
    notes_db.append(new_note) # add the new note to the in-memory database
    return new_note


@router.get("/notes/{note_id}", response_model=Note) # endpoint to retrieve a note by id
def read_note(note_id: UUID):
    """
    Retrieve a note by ID
    """
    for note in notes_db:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found") # raise an error if the note is not found