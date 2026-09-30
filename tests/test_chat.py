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