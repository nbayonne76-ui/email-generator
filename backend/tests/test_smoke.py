from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_repond_ok():
    reponse = client.get("/health")
    assert reponse.status_code == 200
    assert reponse.json() == {"status": "ok"}


def test_racine_repond():
    assert client.get("/").status_code == 200
