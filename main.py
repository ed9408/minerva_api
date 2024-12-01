import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import create_all_tables
from src.routes import auth, user

allowed_origins = os.environ.get("ORIGINS").split(",")
allowed_methods = os.environ.get("METHODS").split(",")

app = FastAPI(
    lifespan=create_all_tables,
    title="Minerva API",
    description="Minerva backend",
    version="1.0.0",
    root_path="/api/v1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=allowed_methods,
    allow_headers=['content-type', 'authorization'],
)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Minerva API"}
