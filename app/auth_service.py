from postgres import user_repository
from app.security_utils import verify_password


def authenticate(db, username: str, password: str):
    user = user_repository.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
