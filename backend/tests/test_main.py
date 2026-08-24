import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "NEO VPN API"

def test_get_prices():
    response = client.get("/payment/prices")
    assert response.status_code == 200
    data = response.json()
    assert "basic" in data
    assert "pro" in data