import pytest
from pydantic import ValidationError
from app.schemas.items import ItemCreate, Item

def test_item_create_valid():
    item_data = {
        "name": "Test Item",
        "description": "Test Description",
        "quantity": 10,
        "category_id": 1
    }
    item = ItemCreate(**item_data)
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert item.quantity == 10
    assert item.category_id == 1

def test_item_create_minimal():
    item_data = {
        "name": "Test Item",
        "quantity": 10,
        "category_id": 1
    }
    item = ItemCreate(**item_data)
    assert item.name == "Test Item"
    assert item.description is None
    assert item.quantity == 10
    assert item.category_id == 1

def test_item_create_invalid_quantity():
    with pytest.raises(ValidationError):
        ItemCreate(
            name="Test Item",
            quantity="invalid",  # Should be int
            category_id=1
        )

def test_item_create_missing_required():
    with pytest.raises(ValidationError):
        ItemCreate(
            name="Test Item"  # Missing required fields
        )

def test_item_response_valid():
    item_data = {
        "id": 1,
        "name": "Test Item",
        "description": "Test Description",
        "quantity": 10,
        "category_id": 1
    }
    item = Item(**item_data)
    assert item.id == 1
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert item.quantity == 10
    assert item.category_id == 1 