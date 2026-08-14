from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Transaction, TransactionPublic, TransactionBase, TransactionUpdate


router = APIRouter(
    prefix="/api",
    tags=["transactions"]
)

# ===========================================================================
# READ METHODS
# ===========================================================================
@router.get("/transaction/all", response_model=list[TransactionPublic])
def read_all_transactions(session: Session = Depends(get_session)):
    """
    Reads all transactions from the database.

    Returns:
        List of all transactions.
    """
    transactions = session.exec(select(Transaction)).all()
    return transactions


@router.get("/transaction/{tr_id}", response_model=TransactionPublic)
def read_transaction_by_id(tr_id: int, session: Session = Depends(get_session)):
    """
    Reads a transaction from the database by its ID.

    Args:
        tr_id: The ID of the transaction to read.

    Returns:
        The transaction with the specified ID.
    """
    transaction = session.get(Transaction, tr_id)
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction {tr_id} not found")
    return transaction


# ===========================================================================
# CREATE METHOD
# ===========================================================================
@router.post("/transaction/", response_model=TransactionPublic)
def create_transaction(transaction: TransactionBase, session: Session = Depends(get_session)):
    """
    Creates a new transaction in the database.

    Args:
        transaction: The transaction to create.

    Returns:
        The created transaction.
    """
    db_transaction = Transaction.model_validate(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction) # db_transaction now has id
    return db_transaction


# ===========================================================================
# UPDATE METHOD
# ===========================================================================
@router.patch("/transaction/{tr_id}", response_model=TransactionPublic)
def update_transaction_by_id(tr_id: int, payload_transaction: TransactionUpdate, session: Session = Depends(get_session)):
    """
    Updates a transaction in the database.

    Args:
        tr_id: The ID of the transaction to update.
        payload_transaction: The transaction to update.

    Returns:
        The updated transaction.
    """
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


# ===========================================================================
# DELETE METHOD
# ===========================================================================
@router.delete("/transaction/{tr_id}")
def delete_transaction_by_id(tr_id: int, session: Session = Depends(get_session)):
    """
    Deletes a transaction from the database.

    Args:
        tr_id: The ID of the transaction to delete.

    Returns:
        A dictionary indicating that the deletion was successful.
    """
    transaction = session.get(Transaction, tr_id)
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction {tr_id} not found")

    session.delete(transaction)
    session.commit()
    return {"delete_ok":True}