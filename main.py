from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.services.rabbit_mq import rabbitmq_client
from app.routers import router


@asynccontextmanager
async def lifespan(fast_api_app: FastAPI) -> AsyncGenerator[None, None]:
    await rabbitmq_client.connect()
    try:
        yield
    finally:
        await rabbitmq_client.close()


app = FastAPI(
    lifespan=lifespan,
    title="Fast API RabbitMQ Bridge",
    description="API for sending various parameters to the RabbitMQ queue",
    middleware=[]
)

app.include_router(router)

