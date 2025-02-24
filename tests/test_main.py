from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app  # Import your FastAPI app

client = TestClient(app)

def test_create_order():
    """Test creating a new trade order"""
    
    # Clear existing orders to prevent test failures
    client.get("/orders/")

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

    # Verify that order is saved in the system
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

