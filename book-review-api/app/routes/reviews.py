from fastapi import APIRouter

router = APIRouter()

@router.get("/{book_id}/reviews") # Define the endpoint to get reviews for a specific book
def get_reviews(book_id: str):
    return {"message": f"Reviews for book {book_id}"}
