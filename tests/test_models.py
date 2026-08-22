from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_models():

    response = client.get("/models")

    assert response.status_code == 200

    data = response.json()

    assert "models" in data

    assert isinstance(data["models"], list)

    assert "openai/gpt-oss-20b" in data["models"]