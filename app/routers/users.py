from typing import List
from fastapi import APIRouter, status
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
            roles=str(db_user.role).split(" "),
        )
        for db_user in db_users
    ]


@router.get("/{user_id}")
async def get_user(user_id: int, duckdb: SqlAlchemySessionDep) -> UserResponse:
    db_user = duckdb.query(User).get(user_id)

    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        roles=str(db_user.role).split(" "),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user: UserCreate, duckdb: SqlAlchemySessionDep) -> UserResponse:
    db_user = User(
        username=user.username,
        email=user.email,
        password=bcrypt.hashpw(
            user.password.get_secret_value().encode("utf-8"), bcrypt.gensalt()
        ),
        role=" ".join(sorted(user.roles)),
    )

    duckdb.add(db_user)
    duckdb.commit()
    duckdb.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        roles=str(db_user.role).split(" "),
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, duckdb: SqlAlchemySessionDep):
    db_user = duckdb.query(User).get(user_id)
    duckdb.delete(db_user)
    duckdb.commit()
