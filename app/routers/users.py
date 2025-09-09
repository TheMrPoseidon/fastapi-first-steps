from typing import List
from fastapi import APIRouter, status
from fastapi.responses import Response

import bcrypt

from ..dependencies import SqlAlchemySessionDep
from ..schemas.users import UserResponse, UserCreate, UserUpdate

from ..models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("")
async def get_users(duckdb: SqlAlchemySessionDep) -> List[UserResponse]:
    users = duckdb.query(User).all()

    return [user.to_response() for user in users]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserCreate, duckdb: SqlAlchemySessionDep) -> UserResponse:
    user = User(
        username=user.username,
        email=user.email,
        password=bcrypt.hashpw(
            user.password.get_secret_value().encode("utf-8"), bcrypt.gensalt()
        ),
        roles=user.roles,
    )

    duckdb.add(user)
    duckdb.commit()
    duckdb.refresh(user)

    return user.to_response()


@router.get("/{user_id}")
async def get_user(user_id: int, duckdb: SqlAlchemySessionDep) -> UserResponse:
    user: User = duckdb.query(User).get(user_id)

    return user.to_response()


@router.put("/{user_id}")
async def update_user(
    user_id: int, update: UserUpdate, duckdb: SqlAlchemySessionDep
) -> UserResponse:
    user: User = duckdb.query(User).get(user_id)

    if update.email is not None:
        user.email = update.email
    if update.roles is not None:
        user.roles = update.roles
    if update.password is not None:
        user.password = bcrypt.hashpw(
            user.password.get_secret_value().encode("utf-8"), bcrypt.gensalt()
        )

    duckdb.commit()
    duckdb.refresh(user)

    return user.to_response()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, duckdb: SqlAlchemySessionDep) -> Response:
    user = duckdb.query(User).get(user_id)
    duckdb.delete(user)
    duckdb.commit()

    return Response()
