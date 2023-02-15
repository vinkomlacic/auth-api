from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import schemas
from app.security_utils import decode_token
from postgres.user_repository import UserRepository
from postgres.database import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[schemas.User]:
    """
    Retrieves the current user from the provided access token and verifies it exists in the database.

    If the user does not exist in the database, this function silently fails and returns None.
    """
    user_base = decode_token(token)

    user_repository = UserRepository(db)
    user = user_repository.get_user_by_username(user_base.username)

    return user
