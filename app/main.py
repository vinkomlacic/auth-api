from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, auth_service, dependencies as deps
from app.security_utils import create_access_token
from app.config import settings
from postgres import models
from postgres.user_repository import UserRepository
from postgres.database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    """Creates user from the provided data. If the username already exists, raises an error."""
    user_repository = UserRepository(db)

    db_user = user_repository.get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    return user_repository.create_user(user=user)


@app.post("/token", response_model=schemas.Token)
def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    """Authenticates the user and if the authentication passes, returns a re-usable access token."""
    user = auth_service.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # If credentials are valid, create a token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
def get_users_me(current_user: schemas.User = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    """Gets the currently logged-in user. If the user does not exist, raises an error."""
    user_repository = UserRepository(db)

    db_user = user_repository.get_user(current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
