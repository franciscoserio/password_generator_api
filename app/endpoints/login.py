from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from app.utils.exceptions import AuthorizationException
from app.utils import get_db
from app.schemas import Login, Token
from app.utils.data_handlers import UserDataHandler
from app.services import AuthenticationService

router = APIRouter()


@router.post("/api/login/", status_code=status.HTTP_200_OK, response_model=Token)
def get_access_token(user: Login, db: Session = Depends(get_db)):
    authentication_service = AuthenticationService(
        email=user.email, password=user.password, user_data_handler=UserDataHandler(db)
    )
    authentication_service.run()
    if authentication_service.token is not None:
        return Token(token=authentication_service.token)
    raise AuthorizationException("Credentials are incorrect")
