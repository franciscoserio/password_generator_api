from pydantic import BaseModel, validator
from datetime import datetime

from app.utils.configs import MIN_PASSWORD_LENGHT, MAX_PASSWORD_LENGHT
from . import User


class ConfigurationCreate(BaseModel):
    lenght: int
    numbers: bool
    lowercase_chars: bool
    uppercase_chars: bool
    special_symbols: bool
    is_active: bool

    @validator("lenght")
    def validate_lenght(cls, value):
        if value > MAX_PASSWORD_LENGHT or value < MIN_PASSWORD_LENGHT:
            raise ValueError("must be higher that 0 and less than or equals to 200")
        return value


class ConfigurationUpdate(ConfigurationCreate):
    lenght: int = None
    numbers: bool = None
    lowercase_chars: bool = None
    uppercase_chars: bool = None
    special_symbols: bool = None
    is_active: bool = None


class Configuration(BaseModel):
    id: int
    lenght: int
    numbers: bool
    lowercase_chars: bool
    uppercase_chars: bool
    special_symbols: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime = None
    user: User

    class Config:
        orm_mode = True
