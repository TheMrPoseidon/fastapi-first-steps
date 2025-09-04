from typing import List, Annotated
from pydantic import BaseModel, EmailStr, SecretStr, StringConstraints


class UserBase(BaseModel):
    username: str
    email: EmailStr
    roles: List[
        Annotated[str, StringConstraints(pattern="^(?:(?<tenant>[a-zA-Z]+)\.)?(?<action>[a-zA-Z]+)$")]
    ] = ["user"]


class UserCreate(UserBase):
    password: SecretStr


class UserResponse(UserBase):
    id: int
