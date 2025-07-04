from uuid import uuid4
from datetime import datetime

# In-memory databases
books_db = []
reviews_db = []

# Sample structure
books_db = [
    {
        "id": str(uuid4()),
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "genre": "Programming",
        "published_year": 2008
    },
    {
        "id": str(uuid4()),
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "Self-help",
        "published_year": 2018
    }
]


# Match reviews to book IDs from above
reviews_db = [
    {
        "id": str(uuid4()),
        "book_id": books_db[0]["id"],
        "reviewer": "Alice",
        "rating": 5,
        "text": "Great book for writing better code!",
        "created_at": datetime.utcnow()
    },
    {
        "id": str(uuid4()),
        "book_id": books_db[0]["id"],
        "reviewer": "Bob",
        "rating": 4,
        "text": "Very detailed and practical.",
        "created_at": datetime.utcnow()
    },
    {
        "id": str(uuid4()),
        "book_id": books_db[1]["id"],
        "reviewer": "Charlie",
        "rating": 5,
        "text": "Life-changing ideas, highly recommended.",
        "created_at": datetime.utcnow()
    }
]



# --Utility functions--

# Find a book by ID
def find_book_by_id(book_id: str):
    return next((book for book in books_db if book["id"] == book_id), None)

# Find reviews by book ID
def find_reviews_by_book_id(book_id: str):
    return [review for review in reviews_db if review["book_id"] == book_id]