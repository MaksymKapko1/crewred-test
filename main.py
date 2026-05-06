from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import create_tables
from app.api.endpoints import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)