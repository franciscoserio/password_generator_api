from pydantic import BaseModel


class RandomPassword(BaseModel):
    random_password: str
