from fastapi import APIRouter, HTTPException
from app.models import books_db, find_book_by_id, reviews_db, find_reviews_by_book_id
from app.schemas import Review, ReviewCreate
from datetime import datetime
from uuid import uuid4
from typing import Optional

router = APIRouter()

@router.get("/{book_id}/reviews", response_model=list[Review]) 
def get_reviews(
    book_id: str,
    rating: Optional[int] = None,
    reviewer: Optional[str] = None,
    min_rating: Optional[int] = None
):
    """Get all reviews for a specific book by its ID"""
    if not find_book_by_id(book_id): # check if the book exists
        raise HTTPException(status_code=404, detail="Book not found") # raise an error if the book does not exist
    
    results = [r for r in reviews_db if r["book_id"] == book_id] # filter reviews by book ID

    # filter reviews based on rating, min_rating, and reviewer
    if rating is not None:
        results = [r for r in results if r["rating"] == rating]
    if min_rating is not None:
        results = [r for r in results if r["rating"] >= min_rating]
    if reviewer:
        results = [r for r in results if r["reviewer"].lower() == reviewer.lower()]

    return results


@router.post("/{book_id}/reviews", response_model=Review, status_code=201)
def create_review(book_id: str, review: ReviewCreate):
    """Create a new review for a specific book by its ID"""
    if not find_book_by_id(book_id): # check if the book exists
        raise HTTPException(status_code=404, detail="Book not found") # raise an error if the book does not exist

    new_review = review.dict() # convert the review to a dictionary
    new_review["id"] = str(uuid4()) # generate a unique ID for the review
    new_review["book_id"] = book_id # associate the review with the book
    new_review["created_at"] = datetime.utcnow() # set the creation time of the review
    reviews_db.append(new_review) # add the new review to the database
    return new_review # return the newly created review
