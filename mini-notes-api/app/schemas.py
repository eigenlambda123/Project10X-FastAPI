from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime, timezone


class NoteBase(BaseModel):
    """
    Base model for a note, containing common fields.
    """
    title: str = Field(..., min_length=1, max_length=100, example="Meeting notes") # Title of the note
    content: str = Field(..., min_length=1, example="Discuss project updates") # Content of the note
    tags: Optional[List[str]] = Field(default=None, description="List of tags associated with the note", example=["work", "personal"]) # tags for the note


class NoteCreate(NoteBase):
    """
    Model for creating a new note.
    Inherits from NoteBase and can include additional fields if needed.
    """
    pass


class NoteUpdate(BaseModel):
    """
    Model for updating an existing note
    Inherits from BaseModel and allows partial updates
    """
    title: Optional[str] = Field(None, max_length=100) # Optional title for the note, can be updated
    content: Optional[str] = None # Optional content for the note, can be updated
    tags: Optional[List[str]] = None # Optional list of tags for the note, can be updated


class Note(NoteBase):
    """
    Model for a note that includes an ID.
    Inherits from NoteBase and adds an ID field.
    """
    id: UUID = Field(default_factory=uuid4) # Unique identifier for the note, generated randomly using uuid4 for each new instance
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) # Timestamp when the note was created in UTC for consistency in distributed systems

    class Config:
        """
        Example configuration for the Note model.
        This includes ORM mode for compatibility with ORMs like SQLAlchemy and an example schema.
        """
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Meeting Notes",
                "content": "Discussed project roadmap and deadlines.",
                "tags": ["work", "urgent"],
                "created_at": "2024-06-18T12:34:56.789Z"
            }
        }
