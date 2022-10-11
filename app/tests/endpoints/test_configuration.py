from fastapi.testclient import TestClient

USER_EMAIL = "example@example.com"
USER_PASSWORD = "password"


def test_create_configuration_ok(
    client: TestClient,
):
    create_configuration = _add_configuration(client)
    assert create_configuration.status_code == 201


def test_create_configuration_missing_access_token(
    client: TestClient,
):
    payload = {
        "lenght": 10,
        "numbers": False,
        "lowercase_chars": True,
        "uppercase_chars": True,
        "special_symbols": True,
        "is_active": True,
    }
    response = client.post("/api/admin/configurations/", json=payload)
    assert response.status_code == 401


def test_create_configuration_missing_fields(
    client: TestClient,
):
    token = _get_token(client)
    payload = {
        "lenght": 10,
        "numbers": False,
        "uppercase_chars": True,
        "special_symbols": True,
        "is_active": True,
    }
    headers = {"Authorization": "Bearer " + token}
    response = client.post("/api/admin/configurations/", json=payload, headers=headers)
    assert response.status_code == 422


def test_create_configuration_higher_lenght(
    client: TestClient,
):
    token = _get_token(client)
    payload = {
        "lenght": 300,
        "numbers": False,
        "lowercase_chars": True,
        "uppercase_chars": True,
        "special_symbols": True,
        "is_active": True,
    }
    headers = {"Authorization": "Bearer " + token}
    response = client.post("/api/admin/configurations/", json=payload, headers=headers)
    assert response.status_code == 422


def test_get_list_configurations_without_token(
    client: TestClient,
):
    response = client.get("/api/admin/configurations/")
    assert response.status_code == 401


def test_get_list_configurations_ok(
    client: TestClient,
):
    _ = _add_configuration(client)
    token = _get_token(client)
    headers = {"Authorization": "Bearer " + token}
    response = client.get("/api/admin/configurations/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_inexistent_specific_configuration(
    client: TestClient,
):
    token = _get_token(client)
    headers = {"Authorization": "Bearer " + token}
    response = client.get("/api/admin/configurations/1", headers=headers)
    assert response.status_code == 404


def test_get_specific_configuration_without_token(
    client: TestClient,
):
    response = client.get("/api/admin/configurations/1")
    assert response.status_code == 401


def test_get_specific_configuration_ok(
    client: TestClient,
):
    created_configuration = _add_configuration(client).json()
    token = _get_token(client)
    headers = {"Authorization": "Bearer " + token}
    response = client.get(
        f"/api/admin/configurations/{str(created_configuration['id'])}/",
        headers=headers,
    )
    assert response.status_code == 200


def test_update_specific_configuration_ok(
    client: TestClient,
):
    created_configuration = _add_configuration(client).json()
    token = _get_token(client)
    headers = {"Authorization": "Bearer " + token}
    payload = {"lenght": 123}
    response = client.patch(
        f"/api/admin/configurations/{str(created_configuration['id'])}/",
        json=payload,
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["lenght"] == 123


def test_update_specific_configuration_without_access_token(
    client: TestClient,
):
    created_configuration = _add_configuration(client).json()
    payload = {"lenght": 123}
    response = client.patch(
        f"/api/admin/configurations/{str(created_configuration['id'])}/", json=payload
    )
    assert response.status_code == 401


def test_delete_specific_configuration_ok(
    client: TestClient,
):
    created_configuration = _add_configuration(client).json()
    token = _get_token(client)
    headers = {"Authorization": "Bearer " + token}
    response = client.delete(
        f"/api/admin/configurations/{str(created_configuration['id'])}/",
        headers=headers,
    )
    assert response.status_code == 204


def test_delete_specific_configuration_without_token(
    client: TestClient,
):
    response = client.delete("/api/admin/configurations/1/")
    print(response.content)
    assert response.status_code == 401


def _add_user(client: TestClient) -> None:
    payload = {"email": USER_EMAIL, "password": USER_PASSWORD}
    client.post("/api/signup/", json=payload)


def _get_token(client: TestClient) -> str:
    _add_user(client)
    payload = {"email": USER_EMAIL, "password": USER_PASSWORD}
    resp = client.post("/api/login/", json=payload)
    return resp.json()["token"]


def _add_configuration(client: TestClient) -> TestClient:
    token = _get_token(client)
    payload = {
        "lenght": 10,
        "numbers": False,
        "lowercase_chars": True,
        "uppercase_chars": True,
        "special_symbols": True,
        "is_active": True,
    }
    headers = {"Authorization": "Bearer " + token}
    return client.post("/api/admin/configurations/", json=payload, headers=headers)
