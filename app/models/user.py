from sqlalchemy import Column, Integer, String, Sequence, JSON
from ..database import Base
from ..schemas.users import UserResponse


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    roles = Column(JSON, nullable=False, default=list)

    def to_response(self) -> UserResponse:
        return UserResponse(
            id=self.id,
            username=self.username,
            email=self.email,
            roles=self.roles,
        )
