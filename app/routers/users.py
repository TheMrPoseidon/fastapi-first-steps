from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

import bcrypt

from ..dependencies import SqlAlchemySessionDep
from ..schemas.users import UserResponse, UserCreate

from ..models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("")
async def get_users(duckdb: SqlAlchemySessionDep) -> List[UserResponse]:
    db_users = duckdb.query(User).all()

    return [
        UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            roles=db_user.role,
        )
        for db_user in db_users
    ]


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
        role=user.roles,
    )

    duckdb.add(user)
    duckdb.commit()
    duckdb.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        roles=user.role,
    )


@router.get("/{user_id}")
async def get_user(user_id: int, duckdb: SqlAlchemySessionDep) -> UserResponse:
    user = duckdb.query(User).get(user_id)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        roles=user.role,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, duckdb: SqlAlchemySessionDep) -> Response:
    user = duckdb.query(User).get(user_id)
    duckdb.delete(user)
    duckdb.commit()

    return Response()
