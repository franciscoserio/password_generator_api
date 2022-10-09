from typing import Optional
from app.utils.data_handlers import UserDataHandler
from app.utils import create_access_token
from .base import BaseService


class AuthenticationService(BaseService):
    """
    Class that handles the user authentication to be used by login endpoint.
    It must be initialized with the following parameters:
    email, password and user_data_handler
    """

    def __init__(
        self, email: str, password: str, user_data_handler: UserDataHandler
    ) -> None:
        super().__init__()
        self.email: str = email
        self.password: str = password
        self.user_data_handler: UserDataHandler = user_data_handler
        self.token: Optional[str] = None

    def run(self) -> None:
        if self._validate_credentials():
            self.token = self._get_access_token()

    def _validate_credentials(self) -> bool:
        if self.user_data_handler.valid_credentials(self.email, self.password):
            return True
        return False

    def _get_access_token(self) -> str:
        data = dict()
        data["email"] = self.email
        return create_access_token(data)
