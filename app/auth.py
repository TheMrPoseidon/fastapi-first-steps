import os
import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from .dependencies import SqlAlchemySessionDep
from .models.user import User
from .schemas.users import UserResponse
from .schemas.tokens import Token

load_dotenv()

SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET")
ALGORITHM = os.getenv("ACCESS_TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user_by_token(
    token: Annotated[str, Depends(oauth2_scheme)], db: SqlAlchemySessionDep
) -> UserResponse:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_name = payload.get("sub")
    return db.query(User).filter(User.email == user_name).first()


UserSessionDep = Annotated[UserResponse, Depends(get_current_user_by_token)]

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token")
async def login_for_access_token(
    oauth2_request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SqlAlchemySessionDep,
) -> Token:
    user = db.query(User).filter(User.username == oauth2_request.username).first()
    if not user or not verify_password(oauth2_request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = {
        "sub": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return Token(
        access_token=jwt.encode(payload, SECRET_KEY, ALGORITHM), token_type="bearer"
    )
