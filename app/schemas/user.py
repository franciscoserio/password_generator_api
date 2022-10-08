from pydantic import BaseModel, validator
from app.utils import validate_email


class UserCreate(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, value):
        if not validate_email(value):
            raise ValueError("must be a valid email")
        return value.title()

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("must contain at least 8 characters")
        return value.title()


class User(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        orm_mode = True
