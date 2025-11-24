from fastapi import APIRouter, status
from fastapi.responses import Response

from ..auth import UserSessionDep, hash_password
from ..dependencies import SqlAlchemySessionDep
from ..models.user import User
from ..schemas.users import UserResponse, UserCreate, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("")
async def get_users(db: SqlAlchemySessionDep) -> list[UserResponse]:
    users = db.query(User).all()

    return [user.to_response() for user in users]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(create: UserCreate, db: SqlAlchemySessionDep) -> UserResponse:
    user = User(
        username=create.username,
        email=create.email,
        password=hash_password(create.password.get_secret_value()),
        roles=create.roles,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user.to_response()


@router.get("/me")
async def get_current_user(user_session: UserSessionDep) -> UserResponse:
    return user_session


@router.get("/{user_id}")
async def get_user(user_id: int, db: SqlAlchemySessionDep) -> UserResponse:
    user: User = db.query(User).get(user_id)

    return user.to_response()


@router.put("/{user_id}")
async def update_user(
    user_id: int, update: UserUpdate, db: SqlAlchemySessionDep
) -> UserResponse:
    user: User = db.query(User).get(user_id).first()

    if update.email is not None:
        user.email = update.email
    if update.roles is not None:
        user.roles = update.roles
    if update.password is not None:
        user.password = (hash_password(update.password.get_secret_value()),)

    db.commit()
    db.refresh(user)

    return user.to_response()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: SqlAlchemySessionDep) -> Response:
    user = db.query(User).get(user_id)
    db.delete(user)
    db.commit()

    return Response()
