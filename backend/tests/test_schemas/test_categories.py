import pytest
from pydantic import ValidationError
from app.schemas.categories import CategoryCreate, Category

def test_category_create_valid():
    category_data = {
        "name": "Test Category",
        "description": "Test Description"
    }
    category = CategoryCreate(**category_data)
    assert category.name == "Test Category"
    assert category.description == "Test Description"

def test_category_create_minimal():
    category_data = {
        "name": "Test Category"
    }
    category = CategoryCreate(**category_data)
    assert category.name == "Test Category"
    assert category.description is None

def test_category_create_invalid():
    with pytest.raises(ValidationError):
        CategoryCreate()  # Missing required name field

def test_category_response_valid():
    category_data = {
        "id": 1,
        "name": "Test Category",
        "description": "Test Description"
    }
    category = Category(**category_data)
    assert category.id == 1
    assert category.name == "Test Category"
    assert category.description == "Test Description" 