from fastapi import FastAPI
from app.routes import books, reviews 

app = FastAPI(title="Book Review API")

# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Book Review API is running"}


# Mount the routers
app.include_router(books.router, prefix="/books", tags=["Books"]) # Mounting books router
app.include_router(reviews.router, prefix="/books", tags=["Reviews"]) # Mounting reviews router