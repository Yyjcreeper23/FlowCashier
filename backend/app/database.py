from pathlib import Path
from sqlmodel import create_engine, Session, SQLModel


# Path to the directory containing this file
# This ensures transaction.db is always created at backend
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "transaction.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

def create_db_and_tables():
    """
    Creating the database and tables for the app
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Yields a session object (should be used with Depends[])
    """
    with Session(engine) as session:
        yield session