from fastapi.testclient import TestClient


def test_login_wrong_credentials(
    client: TestClient,
):
    payload = {"email": "example@example.com", "password": "password"}
    response = client.post("/api/login/", json=payload)
    assert response.status_code == 401


def test_login_credentials_ok(
    client: TestClient,
):
    payload = {"email": "example@example.com", "password": "password"}
    # add an user
    client.post("/api/signup/", json=payload)
    response = client.post("/api/login/", json=payload)
    assert response.status_code == 200
