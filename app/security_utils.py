from datetime import datetime, timedelta
from typing import Union

from jose import jwt
from passlib.context import CryptContext

from app import schemas
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=15)

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(jwt_token) -> schemas.UserBase:
    decoded_jwt = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return schemas.UserBase(username=decoded_jwt['sub'])
