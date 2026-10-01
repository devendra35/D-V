from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_chat_rejects_empty_message():
    response = client.post(
        "/chat",
        json={"message": ""},
    )

    assert response.status_code == 422


def test_chat_rejects_oversized_message():
    response = client.post(
        "/chat",
        json={"message": "A" * 4001},
    )

    assert response.status_code == 422


def test_chat_rejects_long_session_id():
    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "session_id": "S" * 101,
        },
    )

    assert response.status_code == 422


def test_chat_rejects_invalid_json():
    response = client.post(
        "/chat",
        content="not-json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


def test_chat_open_project_returns_action(monkeypatch):
    response = client.post(
        "/chat",
        json={
            "message": "Open Brain Tumor Analyzer"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["action"] is not None
    assert data["action"]["type"] == "OPEN_PROJECT"
    assert data["action"]["project_id"] == "brain-tumor-analyzer"


def test_chat_filter_projects_returns_action():
    response = client.post(
        "/chat",
        json={
            "message": "Show me AI projects"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["action"] is not None
    assert data["action"]["type"] == "FILTER_PROJECTS"
    assert data["action"]["category"] == "AI/ML"


def test_chat_normal_question_has_no_action():
    response = client.post(
        "/chat",
        json={
            "message": "Who is Devendra?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["action"] is None
def test_chat_download_resume_returns_action():
    response = client.post(
        "/chat",
        json={
            "message": "Download my resume"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["action"] is not None
    assert data["action"]["type"] == "DOWNLOAD_RESUME"
