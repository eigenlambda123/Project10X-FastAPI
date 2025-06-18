from fastapi import APIRouter
from app.schemas import Note
from app.models import notes_db

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