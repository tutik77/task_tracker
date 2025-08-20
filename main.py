from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.database.database import init_db
from src.api.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
