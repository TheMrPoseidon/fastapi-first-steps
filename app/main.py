from dotenv import load_dotenv
from fastapi import FastAPI
from .routers import health, users

from .database import Base, engine
load_dotenv()

async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(users.router)
