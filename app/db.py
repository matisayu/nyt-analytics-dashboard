import sys
import os
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

# Ensure tables exist before aggregation
def init_db():
    SQLModel.metadata.create_all(engine)

# Keeps compatibility with FastAPI (generator-style)
def get_session():
    with Session(engine) as session:
        yield session

# Contextmanager for scripts and CLI tools
@contextmanager
def session_context():
    """Context manager for use in scripts and batch jobs."""
    with Session(engine) as session:
        yield session
