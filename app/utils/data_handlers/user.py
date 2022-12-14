from typing import Optional
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate
from app.utils.data_handlers.base import BaseDataHandler
from app.utils.generate_user_password import GenerateUserPassword


class UserDataHandler(BaseDataHandler):
    """
    Class with useful methods regarding a user such as
    adding a user to the database, getting a user instance, etc.
    """

    def __init__(self, db: Session) -> None:
        super().__init__(db)
        self.generate_user_password: GenerateUserPassword = GenerateUserPassword()

    def create_user(self, user: UserCreate) -> User:
        hashed_password = self.generate_user_password.get_password_hash(user.password)
        db_user = User(email=user.email, password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def valid_credentials(self, email: str, password: str) -> bool:
        user = self.get_user_by_email(email)
        if user:
            if (
                self.generate_user_password.verify_password(password, user.password)
                is True
            ):
                return True
        return False
