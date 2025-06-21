from fastapi import APIRouter

router = APIRouter()

@router.get("/") # Define the root endpoint for books
def get_books():
    return {"message": "Books route works"}
