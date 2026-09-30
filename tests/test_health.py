from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "DΞV"
    assert data["message"] == "The AI behind the developer."
    assert data["status"] == "online"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "DΞV"
    assert data["status"] == "online"