from pathlib import Path
from sqlmodel import create_engine, Session, SQLModel, select

from app.example_transactions import example_transactions
from app.models import Transaction


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

    # Add default seed rows if database is empty
    # NOTE: Remove when app is complete
    with Session(engine) as session:
        has_any_rows = session.exec(select(Transaction).limit(1)).first() is not None
        if not has_any_rows:
            for transaction in example_transactions:
                session.add(transaction)
            session.commit()

def get_session():
    """
    Yields a session object (should be used with Depends[])
    """
    with Session(engine) as session:
        yield session