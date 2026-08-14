from app.example_transactions import transactions
from app.models import Transaction, TransactionBase, TransactionPublic
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
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
    """
    Creating the database and tables for the app
    """
    SQLModel.metadata.create_all(engine)

    # Add default seed rows if database is empty
    # NOTE: Remove when app is complete
    with Session(engine) as session:
        has_any_rows = session.exec(select(Transaction).limit(1)).first() is not None
        if not has_any_rows:
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

# READ
@app.get("/transaction/all", response_model=list[TransactionPublic])
def get_all_transactions(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        transactions = session.exec(select(Transaction).offset(offset).limit(limit)).all()
        return transactions

@app.get("/transaction/{tr_id}", response_model=TransactionPublic)
def get_transaction_by_id(tr_id: int):
    with Session(engine) as session:
        transaction = session.get(Transaction, tr_id)
        if not transaction:
            raise HTTPException(status_code=404, detail=f"Transaction {tr_id} not found")
        return transaction

# CREATE
@app.post("/transaction/", response_model=TransactionPublic)
def create_transaction(transaction: TransactionBase):
    with Session(engine) as session:
        db_transaction = Transaction.model_validate(transaction)
        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction) # db_transaction now has id
        return db_transaction

# UPDATE
@app.patch("/transaction/{tr_id}", response_model=TransactionPublic)
def update_transaction_by_id(tr_id: int, payload_transaction: TransactionBase):
    with Session(engine) as session:
        transaction = session.get(Transaction, tr_id)
        if not transaction:
            raise HTTPException(status_code=404, detail=f"Transaction {tr_id} not found")

        updates = payload_transaction.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(transaction, key, value)

        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

# DELETE
@app.delete("/transaction/{tr_id}")
def delete_transaction_by_id(tr_id: int):
    with Session(engine) as session:
        transaction = session.get(Transaction, tr_id)
        if not transaction:
            raise HTTPException(status_code=404, detail=f"Transaction {tr_id} not found")

        session.delete(transaction)
        session.commit()
        return {"delete_ok":True}