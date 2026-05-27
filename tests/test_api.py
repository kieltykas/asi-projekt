import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_api_data_endpoint():
    response = client.get("/api/data")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_404_not_found():
    response = client.get("/nieistniejacy_adres")
    assert response.status_code == 404
