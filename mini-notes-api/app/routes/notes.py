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