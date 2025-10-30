from contextlib import asynccontextmanager

from fastapi import FastAPI

from api_v1 import router as router_v1
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
def hello():
    return {"hello": "world"}

