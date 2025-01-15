import pytest
from app.crud import items
from app.schemas.items import ItemCreate

def test_create_item(db_session):
    item_data = ItemCreate(
        name="Test Item",
        description="Test Description",
        quantity=10,
        category_id=1
    )
    item = items.create_item(db_session, item_data)
    assert item.name == "Test Item"
    assert item.quantity == 10

def test_get_item(db_session):
    # Create test item first
    item_data = ItemCreate(
        name="Test Item",
        description="Test Description",
        quantity=10,
        category_id=1
    )
    created_item = items.create_item(db_session, item_data)
    
    # Now retrieve the item
    item = items.get_item(db_session, item_id=created_item.id)
    assert item is not None
    assert item.id == created_item.id 