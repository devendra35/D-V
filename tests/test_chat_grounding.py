from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_chat_retrieves_known_portfolio_information():
    response = client.post(
        "/chat",
        json={
            "message": (
                "What AI and machine learning projects "
                "has Devendra built?"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    answer = data["response"].lower()

    assert "brain tumor analyzer" in answer
    assert "rag hallucination detector" in answer


def test_chat_does_not_invent_google_employment():
    response = client.post(
        "/chat",
        json={
            "message": (
                "What programming languages does Devendra "
                "use professionally at Google?"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    answer = data["response"].lower()

    assert "google" in answer
    assert (
        "not" in answer
        or "does not" in answer
        or "doesn't" in answer
        or "does not include" in answer
    )


def test_chat_does_not_invent_aws_certification():
    response = client.post(
        "/chat",
        json={
            "message": "What is Devendra's AWS certification?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    answer = data["response"].lower()

    assert "aws" in answer
    assert (
        "not" in answer
        or "does not" in answer
        or "doesn't" in answer
        or "does not include" in answer
    )
