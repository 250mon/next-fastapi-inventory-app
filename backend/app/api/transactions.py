from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import transactions as crud
from app.schemas.transactions import Transaction, TransactionCreate
from app.database import get_db
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/transactions/", response_model=List[Transaction])
def read_transactions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    transactions = crud.get_transactions(db, skip=skip, limit=limit)
    return transactions

@router.get("/transactions/{transaction_id}", response_model=Transaction)
def read_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    transaction = crud.get_transaction(db, transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/items/{item_id}/transactions/", response_model=List[Transaction])
def read_item_transactions(
    item_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    transactions = crud.get_item_transactions(db, item_id=item_id, skip=skip, limit=limit)
    return transactions

@router.post("/transactions/", response_model=Transaction)
def create_transaction(
    transaction: TransactionCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_transaction = crud.create_transaction(db, transaction, current_user.id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_transaction

@router.delete("/transactions/{transaction_id}", response_model=bool)
def delete_transaction(
    transaction_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = crud.delete_transaction(db, transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return success 