from sqlalchemy import Column, Integer, String, Sequence, JSON
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(JSON, nullable=False, default=list)
