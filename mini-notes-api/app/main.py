from fastapi import FastAPI
from app.routes import notes  

app = FastAPI() # Create an instance of FastAPI

app.include_router(notes.router) # Include the notes router

@app.get("/")
def read_root():
    return {"message": "Welcome to Mini Notes API"}
