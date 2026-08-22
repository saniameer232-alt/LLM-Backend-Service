from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat():

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "system_prompt": "You are a helpful assistant.",
            "model": "openai/gpt-oss-20b",
            "temperature": 0.7,
            "max_tokens": 300,
            "history": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert data["model"] == "openai/gpt-oss-20b"
    assert "tokens_used" in data
    assert "latency_ms" in data


def test_chat_with_history():

    response = client.post(
        "/chat",
        json={
            "message": "What is my name?",
            "system_prompt": "You are a helpful assistant.",
            "model": "openai/gpt-oss-20b",
            "temperature": 0.7,
            "max_tokens": 100,
            "history": [
                {
                    "role": "user",
                    "content": "My name is Sania.",
                },
                {
                    "role": "assistant",
                    "content": "Nice to meet you, Sania!",
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "response" in data
    assert data["model"] == "openai/gpt-oss-20b"
    assert "tokens_used" in data
    assert "latency_ms" in data

    assert len(data["response"]) > 0


# -----------------------------------
# Validation Tests
# -----------------------------------


def test_empty_message():

    response = client.post(
        "/chat",
        json={
            "message": "",
            "model": "openai/gpt-oss-20b",
        },
    )

    assert response.status_code == 422


def test_unsupported_model():

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "model": "invalid-model",
        },
    )

    assert response.status_code == 422


def test_invalid_temperature():

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "model": "openai/gpt-oss-20b",
            "temperature": 2.5,
        },
    )

    assert response.status_code == 422


def test_invalid_max_tokens():

    response = client.post(
        "/chat",
        json={
            "message": "Hello",
            "model": "openai/gpt-oss-20b",
            "max_tokens": 0,
        },
    )

    assert response.status_code == 422