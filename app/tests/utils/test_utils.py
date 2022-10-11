from app.utils import validate_email, create_access_token, decode_token


def test_validate_email_ok():
    email = "email@example.com"
    assert validate_email(email) is True


def test_validate_email_not_ok():
    email = "email@example"
    assert validate_email(email) is False


def test_create_access_token():
    assert _create_access_token()


def test_decode_token_ok():
    token = _create_access_token()
    assert decode_token(token)


def test_decode_token_invalid():
    token = "invalid_token"
    assert decode_token(token) is None


def _create_access_token():
    data = dict()
    data["email"] = "email@example.com"
    return create_access_token(data)
