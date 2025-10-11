from contextlib import asynccontextmanager

from core.models import Base, db_helper
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello():
    return {"hello": "world"}

