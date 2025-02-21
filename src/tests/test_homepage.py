from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Welcome to the homepage",
        "data": {},
        "status_code": 200
    }

def test_home_endpoint_wrong_method():
    response = client.post("/")
    assert response.status_code == 405

def test_home_endpoint_headers():
    response = client.get("/")
    assert "application/json" in response.headers["content-type"]