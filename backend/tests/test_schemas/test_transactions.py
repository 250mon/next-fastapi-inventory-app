import pytest
from pydantic import ValidationError
from app.schemas.transactions import TransactionCreate

def test_transaction_create_valid():
    transaction_data = {
        "item_id": 1,
        "quantity_change": 5,
        "transaction_type": "addition"
    }
    transaction = TransactionCreate(**transaction_data)
    assert transaction.item_id == 1
    assert transaction.quantity_change == 5

def test_transaction_create_invalid():
    with pytest.raises(ValidationError):
        TransactionCreate(
            item_id="invalid",  # Should be int
            quantity_change=5,
            transaction_type="addition"
        ) 