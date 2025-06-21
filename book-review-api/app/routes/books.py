from fastapi import APIRouter
from app.models import books_db, find_book_by_id, find_reviews_by_book_id
from app.schemas import Book 
from fastapi import HTTPException

router = APIRouter()

@router.get("/", response_model=list[Book]) 
def get_books():
    """Retrieve a list of all books"""
    return books_db


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: str):
    """
    Retrieve a specific book by its ID, including nested reviews
    """

    book = find_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Include nested reviews
    book["reviews"] = find_reviews_by_book_id(book_id)
    return book