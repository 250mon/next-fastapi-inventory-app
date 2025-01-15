import pytest
from app.crud import transactions, items, categories, auth
from app.schemas.transactions import TransactionCreate
from app.schemas.items import ItemCreate
from app.schemas.categories import CategoryCreate
from app.schemas.auth import UserCreate
from app.api.auth import get_current_user  # Import the dependency we want to override

@pytest.fixture
def test_user(db_session):
    user_data = UserCreate(email="testuser@example.com", password="password123")
    user = auth.create_user(db_session, user_data)
    db_session.refresh(user)
    return user

@pytest.fixture
def test_item(db_session):
    category_data = CategoryCreate(name="Test Category", description="Test Description")
    category = categories.create_category(db_session, category_data)
    db_session.refresh(category)

    item_data = ItemCreate(
        name="Test Item",
        description="Test Description",
        quantity=100,
        category_id=category.id
    )
    item = items.create_item(db_session, item_data)
    db_session.refresh(item)
    return item

@pytest.fixture
def authenticated_client(client, test_user):
    async def override_get_current_user():
        return test_user

    app = client.app
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield client
    app.dependency_overrides = {}

def test_create_transaction(authenticated_client, db_session, test_item, test_user):
    # Use the test_item fixture to get the item_id before any call to the session
    # Otherwise the item_id will be detached from the session
    item_id = test_item.id
    response = authenticated_client.post(
        "/api/transactions/",
        json={
            "item_id": item_id,
            "quantity_change": 10,
            "transaction_type": "addition"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == item_id
    assert data["quantity_change"] == 10
    assert data["transaction_type"] == "addition"

def test_read_transactions(authenticated_client, db_session, test_item, test_user):
    item_id = test_item.id
    # Create some test transactions
    transactions_data = [
        {"item_id": item_id, "quantity_change": 10, "transaction_type": "addition"},
        {"item_id": item_id, "quantity_change": -5, "transaction_type": "subtraction"}
    ]
    for transaction in transactions_data:
        transactions.create_transaction(db_session, TransactionCreate(**transaction), user_id=test_user.id)

    response = authenticated_client.get("/api/transactions/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(transactions_data)
    assert all(tr["item_id"] == item_id for tr in data)

def test_delete_transaction(authenticated_client, db_session, test_item, test_user):
    item_id = test_item.id
    # Create a transaction
    transaction = transactions.create_transaction(
        db_session,
        TransactionCreate(item_id=item_id, quantity_change=10, transaction_type="addition"),
        user_id=test_user.id
    )

    response = authenticated_client.delete(f"/api/transactions/{transaction.id}")
    assert response.status_code == 200
    assert response.json() is True

    # Verify transaction is deleted
    response = authenticated_client.get(f"/api/transactions/{transaction.id}")
    assert response.status_code == 404 