from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").status_code == 200


def test_prix_pass_1_jour():
    assert client.get("/billets").json()["Pass 1 jour"]["prix"] == 59
