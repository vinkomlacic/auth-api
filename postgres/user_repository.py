from sqlalchemy.orm import Session

from app import schemas
from app.security_utils import get_password_hash
from postgres import models


class UserRepository:
    """User repository is responsible for fetching objects from the database."""

    def __init__(self, db: Session):
        self.__db = db

    def get_user(self, user_id: int):
        return self.__db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_username(self, username: str):
        return self.__db.query(models.User).filter(models.User.username == username).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.__db.query(models.User).offset(skip).limit(limit).all()

    def create_user(self, user: schemas.UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = models.User(username=user.username, hashed_password=hashed_password)
        self.__db.add(db_user)
        self.__db.commit()
        self.__db.refresh(db_user)
        return db_user
