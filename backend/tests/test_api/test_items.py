import pytest
from app.crud import items, categories
from app.schemas.items import ItemCreate
from app.schemas.categories import CategoryCreate

@pytest.fixture
def test_category(db_session):
    category_data = CategoryCreate(name="Test Category", description="Test Description")
    category = categories.create_category(db_session, category_data)
    db_session.refresh(category)  # Ensure the category is attached to the session
    return category

def test_create_item(client, db_session, test_category):
    # Use the test_category fixture to get the category_id before any call to the session
    # Otherwise the category_id will be detached from the session
    category_id = test_category.id
    response = client.post(
        "/api/items/",
        json={
            "name": "Test Item",
            "description": "Test Description",
            "quantity": 10,
            "category_id": category_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["quantity"] == 10
    assert data["category_id"] == category_id

def test_read_items(client, db_session, test_category):
    # Create some test items first
    items_data = [
        {"name": "Item 1", "quantity": 10, "category_id": test_category.id},
        {"name": "Item 2", "quantity": 20, "category_id": test_category.id},
        {"name": "Item 3", "quantity": 30, "category_id": test_category.id}
    ]
    for item in items_data:
        items.create_item(db_session, ItemCreate(**item))

    response = client.get("/api/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(items_data)
    assert all(item["name"] in [i["name"] for i in items_data] for item in data)

def test_read_item(client, db_session, test_category):
    item = items.create_item(
        db_session,
        ItemCreate(
            name="Test Item",
            description="Test Description",
            quantity=10,
            category_id=test_category.id
        )
    )

    response = client.get(f"/api/items/{item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["quantity"] == 10

def test_update_item(client, db_session, test_category):
    item = items.create_item(
        db_session,
        ItemCreate(
            name="Original Name",
            description="Original Description",
            quantity=10,
            category_id=test_category.id
        )
    )

    response = client.put(
        f"/api/items/{item.id}",
        json={
            "name": "Updated Name",
            "description": "Updated Description",
            "quantity": 20,
            "category_id": test_category.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["quantity"] == 20

def test_delete_item(client, db_session, test_category):
    item = items.create_item(
        db_session,
        ItemCreate(
            name="Test Item",
            description="Test Description",
            quantity=10,
            category_id=test_category.id
        )
    )

    response = client.delete(f"/api/items/{item.id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verify item is deleted
    response = client.get(f"/api/items/{item.id}")
    assert response.status_code == 404

def test_adjust_item_quantity(client, db_session, test_category):
    item = items.create_item(
        db_session,
        ItemCreate(
            name="Test Item",
            description="Test Description",
            quantity=10,
            category_id=test_category.id
        )
    )

    # Test increasing quantity
    response = client.patch(f"/api/items/{item.id}/quantity?quantity_change=5")
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 15

    # Test decreasing quantity
    response = client.patch(f"/api/items/{item.id}/quantity?quantity_change=-3")
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 12