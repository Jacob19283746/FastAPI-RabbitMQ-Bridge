from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.rabbit import publisher
from app.router import router
from app.settings import settings, setup_logging

setup_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await publisher.connect()
    yield
    await publisher.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "GET-мост: любые query-параметры → нормализация → JSON в очередь RabbitMQ."
    ),
    lifespan=lifespan,
)

app.include_router(router)
