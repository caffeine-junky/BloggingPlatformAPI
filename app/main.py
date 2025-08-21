from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.database import Database
from app.api import v1_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Database.connect(url=settings.DATABASE_URL)
    Database.initialize()
    yield
    Database.disconnect()


app: FastAPI = FastAPI(
    title="Blogging Platform API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
    )
app.include_router(v1_api_router, prefix="/api")


@app.get("/")
def index():
    """"""
    return {"title": app.title}
