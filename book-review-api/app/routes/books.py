from fastapi import APIRouter
from app.models import books_db, find_book_by_id, find_reviews_by_book_id
from app.schemas import Book 
from fastapi import HTTPException
from uuid import uuid4

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





@router.post("/", response_model=Book, status_code=201)
def create_book(book: Book):
    """Create new book"""
    
    new_book = book.model_dump(exclude_unset=True) # Convert Pydantic model to dict, excluding unset fields
    new_book["id"] = str(uuid4()) # Generate a new UUID for the book ID
    books_db.append(new_book) # Add the new book to the in-memory database
    return new_book # Return the newly created book with its ID