from app.utils.generate_user_password import GenerateUserPassword


def test_get_password_hash():
    password_hash = _get_password_hash()
    assert password_hash


def test_verify_password():
    generate_user_password = GenerateUserPassword()
    password_hash = _get_password_hash()
    assert generate_user_password.verify_password("password", password_hash) is True


def _get_password_hash() -> str:
    generate_user_password = GenerateUserPassword()
    return generate_user_password.get_password_hash("password")
