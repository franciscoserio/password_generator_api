from fastapi.testclient import TestClient


def test_signup_missing_fields(
    client: TestClient,
):
    payload = {"password": "password"}
    response = client.post("/api/signup/", json=payload)
    assert response.status_code == 422


def test_signup_wrong_email(
    client: TestClient,
):
    payload = {"email": "email@email", "password": "password"}
    response = client.post("/api/signup/", json=payload)
    assert response.status_code == 422


def test_signup_ok(
    client: TestClient,
):
    payload = {"email": "example@example.com", "password": "password"}
    response = client.post("/api/signup/", json=payload)
    assert response.status_code == 201
