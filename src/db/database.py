import os

from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.engine import Engine
from typing import Any, Generator

from src.core import load_env_file

load_env_file()

engine: Engine

match os.environ.get("ENVIRONMENT"):
    case "development":
        DATABASE_URL = os.environ.get("DATABSE_URL")
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    case "production":
        DATABASE_URL = os.environ.get("DATABSE_URL")
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    case _:
        raise ValueError("Invalid environment")


def create_all_tables(app: FastAPI) -> Generator[None, Any, None]:
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    """Get a session for the database."""
    with Session(engine) as session:
        yield session
