from datetime import datetime, UTC
from sqlalchemy.orm import Session

from app.models import Transaction, Item
from app.schemas.transactions import TransactionCreate

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_item_transactions(db: Session, item_id: int, skip: int = 0, limit: int = 100):
    return db.query(Transaction)\
        .filter(Transaction.item_id == item_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    # First update the item quantity
    item = db.query(Item).filter(Item.id == transaction.item_id).first()
    if item:
        item.quantity += transaction.quantity_change
        
        # Create the transaction record
        db_transaction = Transaction(
            item_id=transaction.item_id,
            quantity_change=transaction.quantity_change,
            transaction_type=transaction.transaction_type,
            transaction_date=datetime.now(UTC),
            user_id=user_id
        )
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    return None

def delete_transaction(db: Session, transaction_id: int):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        # Reverse the quantity change on the item
        item = db.query(Item).filter(Item.id == transaction.item_id).first()
        if item:
            item.quantity -= transaction.quantity_change
            
        db.delete(transaction)
        db.commit()
        return True
    return False 