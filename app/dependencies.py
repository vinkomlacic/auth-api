from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import schemas
from app.security_utils import decode_token
from postgres import user_repository
from postgres.database import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.User:
    """Retrieves the current user from the provided access token."""
    user_base = decode_token(token)

    user = user_repository.get_user_by_username(db, username=user_base.username)

    return user
