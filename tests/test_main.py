from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)

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

def test_get_orders():
    """Test retrieving all orders"""
    response = client.get("/orders/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Ensure response is a list
    assert len(data) > 0  # Ensure at least one order exists
    assert "symbol" in data[0]
    assert "price" in data[0]
    assert "quantity" in data[0]
    assert "order_type" in data[0]

