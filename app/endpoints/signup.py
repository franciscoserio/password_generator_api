from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.utils import get_db
from app.schemas import User, UserCreate
from app.utils.data_handlers import UserDataHandler

router = APIRouter()


@router.post("/api/signup/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_data_handler = UserDataHandler(db)
    if user_data_handler.get_user_by_email(email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return user_data_handler.create_user(user=user)
