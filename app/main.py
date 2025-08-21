from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.database import Database


@asynccontextmanager
async def lifespan(app: FastAPI):
    Database.connect(url=settings.DATABASE_URL)
    Database.initialize()
    yield
    Database.disconnect()


app: FastAPI = FastAPI(title="Blogging Platform API", version="0.1.0", lifespan=lifespan)


@app.get("/")
def index():
    """"""
    return {"title": app.title}
