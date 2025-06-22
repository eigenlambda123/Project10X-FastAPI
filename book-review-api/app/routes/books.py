from fastapi import APIRouter, HTTPException
from app.models import books_db, find_book_by_id, find_reviews_by_book_id
from app.schemas import Book, BookUpdate
from uuid import uuid4
from typing import Optional

router = APIRouter()

# -------------------- READ --------------------

@router.get("/", response_model=list[Book]) 
def get_books(author: Optional[str] = None, genre: Optional[str] = None):
    """Retrieve a list of all books"""
    results = books_db  # start with all books

    # Filter books by author and genre if provided
    if author:
        results = [book for book in results if book.get("author") == author]
    if genre:
        results = [book for book in results if book.get("genre") == genre]

    return results # return the filtered list of books

@router.get("/{book_id}", response_model=Book)
def get_book(
    book_id: str,
    rating: Optional[int] = None,
    reviewer: Optional[str] = None,
    min_rating: Optional[int] = None
):
    """
    Retrieve a specific book by its ID, including nested reviews
    """
    book = find_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    results = [r for r in reviews_db if r["book_id"] == book_id] # filter reviews by book ID

    # Filter reviews based on rating, min_rating, and reviewer parameters
    if rating is not None:
        results = [r for r in results if r["rating"] == rating]
    if min_rating is not None:
        results = [r for r in results if r["rating"] >= min_rating]
    if reviewer:
        results = [r for r in results if r["reviewer"].lower() == reviewer.lower()]

    return results

# -------------------- CREATE --------------------

@router.post("/", response_model=Book, status_code=201)
def create_book(book: Book):
    """Create new book"""
    new_book = book.model_dump(exclude_unset=True)  # Convert Pydantic model to dict, excluding unset fields
    new_book["id"] = str(uuid4())  # Generate a new UUID for the book ID
    books_db.append(new_book)  # Add the new book to the in-memory database
    return new_book  # Return the newly created book with its ID

# -------------------- UPDATE --------------------

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: str, book: BookUpdate):
    """Update an existing book by its ID"""
    existing_book = find_book_by_id(book_id)  # Find the book by ID
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    existing_book.update(book.model_dump(exclude_unset=True))  # Update the book with new data
    return existing_book

# -------------------- DELETE --------------------

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: str):
    """Delete a book by its ID"""
    book = find_book_by_id(book_id)  # Find the book by ID
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db.remove(book)  # Remove the book from the in-memory database
    # Delete associated reviews
    global reviews_db
    reviews_db = [r for r in reviews_db if r["book_id"] != book_id]
