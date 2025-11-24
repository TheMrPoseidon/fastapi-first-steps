from typing import Annotated
from pydantic import BaseModel, EmailStr, SecretStr, StringConstraints

userRolePattern: str = r"^(?:(?<tenant>[a-zA-Z]+)\.)?(?<action>[a-zA-Z]+)$"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    roles: list[
        Annotated[
            str,
            StringConstraints(pattern=userRolePattern),
        ]
    ] = ["user"]


class UserCreate(UserBase):
    password: SecretStr


class UserResponse(UserBase):
    id: int


class UserUpdate(BaseModel):
    email: EmailStr | None
    roles: (
        list[
            Annotated[
                str,
                StringConstraints(pattern=userRolePattern),
            ]
        ]
        | None
    )
    password: SecretStr | None
