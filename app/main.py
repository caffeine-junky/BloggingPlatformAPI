from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app: FastAPI = FastAPI(title="Blogging Platform API", version="0.1.0", lifespan=lifespan)


@app.get("/")
def index():
    """"""
    return {"title": app.title}
