import pytest
from fastapi.testclient import TestClient

from app.main import app

VALID = {"gender": 1, "height_cm": 179, "weight_kg": 91, "morphology": "V"}


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:  # runs lifespan: models load once
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "models_loaded": True}


def test_predict_happy_path(client):
    r = client.post("/predict", json=VALID)
    assert r.status_code == 200
    m = r.json()["measurements"]
    assert {"Chest_Circumference", "Waist_Circumference", "knee", "Head_Circumference"} <= m.keys()
    assert all(isinstance(v, float) and v > 0 for v in m.values())


def test_predict_female(client):
    r = client.post("/predict", json={**VALID, "gender": 0, "morphology": "x"})
    assert r.status_code == 200


@pytest.mark.parametrize(
    "bad",
    [
        {"height_cm": -5},
        {"morphology": "Z"},
        {"gender": 1, "morphology": "A"},  # A is a female-only morphology
        {"weight_kg": "heavy"},
    ],
)
def test_predict_validation_error(client, bad):
    r = client.post("/predict", json={**VALID, **bad})
    assert r.status_code == 422


def test_predict_missing_field(client):
    assert client.post("/predict", json={"gender": 1}).status_code == 422
