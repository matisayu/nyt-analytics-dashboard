import sys
print("Running Python from:", sys.executable)
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./nyt.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
