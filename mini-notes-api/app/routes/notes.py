from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from uuid import UUID

import markdown2
import markdown

from app.schemas import Note, NoteUpdate, NoteCreate
from app.models import notes_db

router = APIRouter()

def render_markdown(note: Note) -> str:
    """
    Render Markdown content to HTML for a given note
    """
    note.rendered_content = markdown2.markdown(note.content) # Convert Markdown content to HTML
    return note # return the note with rendered content


@router.get("/notes", response_model=list[Note]) # endpoint to retrieve all notes
def get_notes(
    search: Optional[str] = Query(None, description="Search notes by title or content"), # optional search query parameter
    limit: int = Query(10, ge=0, description="Maximum number of notes to return"), # optional limit query parameter with a default value of 10
    skip: int = Query(0, ge=0, description="Number of notes to skip") # optional skip query parameter with a default value of 0
):
    """
    - Retrieve all notes with optional search, limit, and pagination
    - If search is provided, filter notes by title or content
    - If limit is provided, return only the specified number of notes
    - If nothing is provided, return all notes
    """
    filtered_notes = notes_db # start with all notes

    if search: # if a search query is provided
        filtered_notes = [
            note for note in notes_db
            if search.lower() in note.title.lower() or search.lower() in note.content.lower()] # filter notes by title or content
    
    # Apply pagination
    paginated_notes = filtered_notes[skip : skip + limit if limit else None]

    # Render Markdown content to HTML for each note in the paginated list
    return [render_markdown(note) for note in paginated_notes]


@router.get("/notes/{note_id}", response_model=Note) # endpoint to retrieve a note by id
def read_note(note_id: UUID):
    """
    Retrieve a note by ID
    """
    for note in notes_db: # iterate through the in-memory database
        if note.id == note_id: # if the note is found
            return note # return the note
    raise HTTPException(status_code=404, detail="Note not found") # raise an error if the note is not found



@router.post("/notes", response_model=Note) # endpoint to create a new note
def create_note(note: NoteCreate):
    """
    Create a new note
    """
    rendered_html = markdown.markdown(note.content) # Convert Markdown content to HTML
    note_data = note.dict() # Convert the NoteCreate schema to a dictionary
    note_data.pop("rendered_content", None)  # Remove rendered_content from the dictionary if it exists

    # Create a new Note object with the provided data and rendered HTML content
    note_obj = Note(
        **note_data, # Unpack the dictionary into the Note model
        rendered_content=rendered_html
    )
    # Save note_obj
    notes_db.append(note_obj)  # Add the new note to the in-memory database
    return note_obj



@router.put("/notes/{note_id}", response_model=Note) # endpoint to update a note by id
def update_note(note_id: UUID, updated_note: NoteUpdate):
    """
    Update a note by ID
    """
    for index, existing_note in enumerate(notes_db): #  find the note to update

        if existing_note.id == note_id: # if the note is found
            note_data = existing_note.model_dump() #  Get the existing note data as a dictionary
            update_data = updated_note.model_dump(exclude_unset=True) # Get the updated data, excluding unset fields


            note_data.update(update_data) # update the existing note data with the new values
            for key, value in update_data.items():
                setattr(existing_note, key, value)  # update fields in place

            return existing_note # return the updated note
        
    raise HTTPException(status_code=404, detail="Note not found") # raise an error if the note is not found



@router.delete("/notes/{note_id}", response_model=Note) # endpoint to delete a note by id
def delete_note(note_id: UUID):
    """
    Delete a note by ID
    """
    for index, existing_note in enumerate(notes_db): #  find the note to delete
        if existing_note.id == note_id: #  if the note is found
            deleted_note = notes_db.pop(index) # remove the note from the in-memory database
            return deleted_note # return the deleted note
        
    raise HTTPException(status_code=404, detail="Note not found") #  raise an error if the note is not found