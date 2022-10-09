from typing import Union
from fastapi import Depends, APIRouter, Query, status
from sqlalchemy.orm import Session

from app.utils import get_db
from app.utils.configs import MIN_PASSWORD_LENGHT, MAX_PASSWORD_LENGHT
from app.utils.data_handlers import ConfigurationDataHandler
from app.services import PasswordGeneratorService
from app.schemas import RandomPassword

router = APIRouter()


@router.get("/api/random-password/", status_code=status.HTTP_200_OK)
def get_random_password(
    lenght: Union[int, None] = Query(
        default=None, ge=MIN_PASSWORD_LENGHT, le=MAX_PASSWORD_LENGHT
    ),
    numbers: bool = None,
    lowercase_chars: bool = None,
    uppercase_chars: bool = None,
    special_symbols: bool = None,
    db: Session = Depends(get_db),
):
    password_generator_service = PasswordGeneratorService(
        lenght=lenght,
        numbers=numbers,
        lowercase_chars=lowercase_chars,
        uppercase_chars=uppercase_chars,
        special_symbols=special_symbols,
        configuration_data_handler=ConfigurationDataHandler(db=db),
    )
    password_generator_service.run()
    return RandomPassword(random_password=password_generator_service.password)
