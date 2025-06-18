from pydantic import BaseModel, Field
from typing import Optional, List


class NoteBase(BaseModel):
    """
    Base model for a note, containing common fields.
    """
    title: str = Field(..., min_length=1, max_length=100) # Title of the note
    content: str = Field(..., min_length=1) # Content of the note
    tags: Optional[List[str]] = Field(default=None, description="List of tags associated with the note") # tags for the note