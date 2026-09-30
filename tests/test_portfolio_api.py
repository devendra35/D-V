from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_profile_endpoint():
    response = client.get("/profile")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Devendra Khanal"
    assert len(data["projects"]) == 5
    assert len(data["skill_categories"]) == 4


def test_projects_endpoint():
    response = client.get("/projects")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 5
    assert data[0]["name"] == "Brain Tumor Analyzer"


def test_single_project_endpoint():
    response = client.get(
        "/projects/brain-tumor-analyzer"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "brain-tumor-analyzer"
    assert data["name"] == "Brain Tumor Analyzer"


def test_unknown_project_returns_404():
    response = client.get(
        "/projects/not-a-real-project"
    )

    assert response.status_code == 404


def test_skills_endpoint():
    response = client.get("/skills")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 29
    assert "Python" in data
    assert "TensorFlow" in data
