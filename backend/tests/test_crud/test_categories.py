import pytest
from sqlalchemy.orm import Session
from app.crud import categories
from app.schemas.categories import CategoryCreate
from app.models import Category

def test_create_category(db_session: Session):
    category_data = CategoryCreate(
        name="Test Category",
        description="Test Description"
    )
    category = categories.create_category(db_session, category_data)
    assert category.name == "Test Category"
    assert category.description == "Test Description"

def test_get_category(db_session: Session):
    # Create a category first
    category_data = CategoryCreate(
        name="Test Category",
        description="Test Description"
    )
    created_category = categories.create_category(db_session, category_data)
    
    # Try to get the category
    category = categories.get_category(db_session, created_category.id)
    assert category is not None
    assert category.name == "Test Category"
    assert category.description == "Test Description"

def test_get_categories(db_session: Session):
    # Create multiple categories
    category_names = ["Category 1", "Category 2", "Category 3"]
    for name in category_names:
        categories.create_category(
            db_session, 
            CategoryCreate(name=name, description=f"Description for {name}")
        )
    
    # Get all categories
    db_categories = categories.get_categories(db_session)
    assert len(db_categories) == len(category_names)
    assert all(c.name in category_names for c in db_categories)

def test_update_category(db_session: Session):
    # Create a category first
    category_data = CategoryCreate(
        name="Original Name",
        description="Original Description"
    )
    created_category = categories.create_category(db_session, category_data)
    
    # Update the category
    update_data = CategoryCreate(
        name="Updated Name",
        description="Updated Description"
    )
    updated_category = categories.update_category(
        db_session, 
        created_category.id, 
        update_data
    )
    
    assert updated_category is not None
    assert updated_category.name == "Updated Name"
    assert updated_category.description == "Updated Description"

def test_delete_category(db_session: Session):
    # Create a category first
    category_data = CategoryCreate(
        name="Test Category",
        description="Test Description"
    )
    created_category = categories.create_category(db_session, category_data)
    
    # Delete the category
    success = categories.delete_category(db_session, created_category.id)
    assert success is True
    
    # Verify category is deleted
    deleted_category = categories.get_category(db_session, created_category.id)
    assert deleted_category is None

def test_delete_nonexistent_category(db_session: Session):
    success = categories.delete_category(db_session, 999)  # Non-existent ID
    assert success is False 