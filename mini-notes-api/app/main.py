from fastapi import FastAPI

app = FastAPI() #  Initialize FastAPI app

@app.get("/") #  Define root endpoint
def read_root(): # Handle GET request to root endpoint
    return {"message": "Mini Notes API is running!"} #  Return a simple JSON response
