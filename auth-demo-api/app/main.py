from fastapi import FastAPI
from app.routes import auth, users

app = FastAPI(title="Auth Demo API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"]) # register auth routes
app.include_router(users.router, prefix="/users", tags=["Users"]) # register user routes

@app.get("/")
def read_root():
    return {"message": "Auth Demo API is running"}