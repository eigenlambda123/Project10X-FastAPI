from fastapi import APIRouter, HTTPException
from app.models import books_db, find_book_by_id, reviews_db, find_reviews_by_book_id
from app.schemas import Review

router = APIRouter()

@router.get("/{book_id}/reviews", response_model=list[Review]) 
def get_reviews(book_id: str):
    """Get all reviews for a specific book by its ID"""
    if not find_book_by_id(book_id): # check if the book exists
        raise HTTPException(status_code=404, detail="Book not found") # raise an error if the book does not exist
    
    return find_reviews_by_book_id(book_id) # return all reviews for the book
