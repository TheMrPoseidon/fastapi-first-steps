from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

from .database import SessionLocal

def get_sqlalchemy_session():
    with SessionLocal() as db:
        yield db
    
SqlAlchemySessionDep = Annotated[Session, Depends(get_sqlalchemy_session)]