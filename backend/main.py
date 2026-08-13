from app.example_transactions import transactions
from app.models import Transaction
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from sqlmodel import create_engine, Session, SQLModel, select

# ===========================================================================
# CREATING THE DATABASE
# ===========================================================================
# Path to the directory containing this file
# This ensures transaction.db is always created at backend
BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "transaction.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

    # Adding all transactions into transaction.db
    with Session(engine) as session:
        for transaction in transactions:
            session.add(transaction)
        session.commit()

# ===========================================================================
# INITIALISING APP
# ===========================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# ===========================================================================
# ADDING MIDDLEWARE
# ===========================================================================
# Middleware to handle different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],    # Vite server
    allow_methods=["*"],
    allow_headers=["*"]
)

# ===========================================================================
# APP METHODS
# ===========================================================================
@app.get("/api/health")
def health():
    return {"status": "ok"}

# Database methods
@app.get("/transaction/all")
def get_all_transactions() -> list[Transaction]:
    with Session(engine) as session:
        return session.exec(select(Transaction)).all()

@app.get("/transaction/{id}")
def get_transaction_by_id(id: int) -> Transaction | None:
    with Session(engine) as session:
        return session.get(Transaction, id)