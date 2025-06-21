from fastapi import APIRouter
from app.models import books_db 
from app.schemas import Book 

router = APIRouter()

@router.get("/", response_model=list[Book]) 
def get_books():
    """Retrieve a list of all books"""
    return books_db
