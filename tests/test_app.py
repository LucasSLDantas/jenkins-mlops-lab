
from fastapi.testclient import TestClient
from app.main import app, APP_VERSION

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["version"] == APP_VERSION


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_positive():
    response = client.post(
        "/predict",
        json={"text": "O produto e excelente"}
    )
    assert response.status_code == 200
    assert response.json()["sentiment"] == "positivo"


def test_negative():
    response = client.post(
        "/predict",
        json={"text": "O produto e ruim"}
    )
    assert response.status_code == 200
    assert response.json()["sentiment"] == "negativo"


def test_neutral():
    response = client.post(
        "/predict",
        json={"text": "O produto chegou"}
    )
    assert response.status_code == 200
    assert response.json()["sentiment"] == "neutro"

