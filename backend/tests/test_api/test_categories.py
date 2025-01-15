import pytest
from app.crud import categories
from app.schemas.categories import CategoryCreate

def test_create_category(client, db_session):
    response = client.post(
        "/api/categories/",
        json={"name": "Test Category", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"
    assert "id" in data

def test_read_categories(client, db_session):
    # Create some test categories first
    categories_data = [
        {"name": "Category 1", "description": "Description 1"},
        {"name": "Category 2", "description": "Description 2"},
        {"name": "Category 3", "description": "Description 3"}
    ]
    for category in categories_data:
        categories.create_category(db_session, CategoryCreate(**category))

    response = client.get("/api/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(categories_data)
    assert all(item["name"] in [cat["name"] for cat in categories_data] for item in data)

def test_update_category(client, db_session):
    category = categories.create_category(
        db_session, 
        CategoryCreate(name="Original Name", description="Original Description")
    )

    response = client.put(
        f"/api/categories/{category.id}",
        json={"name": "Updated Name", "description": "Updated Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated Description"

def test_delete_category(client, db_session):
    category = categories.create_category(
        db_session, 
        CategoryCreate(name="Test Category", description="Test Description")
    )

    response = client.delete(f"/api/categories/{category.id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verify category is deleted
    response = client.get(f"/api/categories/{category.id}")
    assert response.status_code == 404