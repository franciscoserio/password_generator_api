import re


def validate_email(email: str) -> bool:
    email_regex = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(email_regex, email):
        return True
    return False
