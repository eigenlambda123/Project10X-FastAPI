from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime, timezone


class NoteBase(BaseModel):
    """
    Base model for a note, containing common fields.
    """
    title: str = Field(..., min_length=1, max_length=100) # Title of the note
    content: str = Field(..., min_length=1) # Content of the note
    tags: Optional[List[str]] = Field(default=None, description="List of tags associated with the note") # tags for the note

class NoteCreate(NoteBase):
    """
    Model for creating a new note.
    Inherits from NoteBase and can include additional fields if needed.
    """
    pass

class Note(NoteBase):
    """
    Model for a note that includes an ID.
    Inherits from NoteBase and adds an ID field.
    """
    id: UUID = Field(default_factory=uuid4) # Unique identifier for the note, generated randomly using uuid4 for each new instance
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) # Timestamp when the note was created in UTC for consistency in distributed systems