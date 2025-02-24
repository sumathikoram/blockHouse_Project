import os

os.environ["TEST_ENV"] = "true"

from fastapi.testclient import TestClient
from main import app  # Import FastAPI app from main.py
from models import SessionLocal, Base, engine, Order  # Import database models
import httpx


client = TestClient(app)

# Setup: Ensure a fresh database before each test
def setup_module(module):
    """ Clear database before running tests """
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)  # Recreate tables

def test_create_order():
    """Test creating a new trade order"""
    order_data = {
        "symbol": "AAPL",
        "price": 150.5,
        "quantity": 10,
        "order_type": "limit"
    }

    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200

    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["price"] == 150.5
    assert data["quantity"] == 10
    assert data["order_type"] == "limit"
    assert "id" in data  # Ensure order ID is returned

    # Verify that order is saved in the database
    get_response = client.get("/orders/")
    assert get_response.status_code == 200
    orders = get_response.json()
    assert len(orders) > 0
    assert any(o["symbol"] == "AAPL" for o in orders)

def test_get_orders():
    """Test retrieving all orders"""
    response = client.get("/orders/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)  # Ensure response is a list
    assert len(data) > 0  # Ensure at least one order exists
    assert all(k in data[0] for k in ["symbol", "price", "quantity", "order_type"])  # Ensure fields exist
