from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from . import auth
from .routers import health, users
from .database import Base, engine

load_dotenv()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan, title="fastapi-demo", version="0.1.3")
app.include_router(auth.router)

app.include_router(health.router)
app.include_router(users.router)
