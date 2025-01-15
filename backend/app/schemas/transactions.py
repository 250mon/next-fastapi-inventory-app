from datetime import datetime
from pydantic import BaseModel

class TransactionBase(BaseModel):
    item_id: int
    quantity_change: int
    transaction_type: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    transaction_date: datetime
    user_id: int

    class Config:
        from_attributes = True 