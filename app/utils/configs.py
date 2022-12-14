import os

# Database
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_PORT = os.environ.get("DATABASE_PORT")

# algorithm for jwt token
ALGORITHM = "HS256"

SECRET_KEY_DEFAULT = "test"
SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY_DEFAULT)

# ACCESS_TOKEN_EXPIRE_MINUTES
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
except ValueError:
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

# MIN_PASSWORD_LENGHT
try:
    MIN_PASSWORD_LENGHT = int(os.environ.get("MIN_PASSWORD_LENGHT", 1))
except ValueError:
    MIN_PASSWORD_LENGHT = 1

# MAX_PASSWORD_LENGHT
try:
    MAX_PASSWORD_LENGHT = int(os.environ.get("MAX_PASSWORD_LENGHT", 200))
except ValueError:
    MAX_PASSWORD_LENGHT = 200
