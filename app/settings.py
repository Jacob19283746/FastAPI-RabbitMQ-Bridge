from __future__ import annotations

import logging
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_ignore_empty=True,
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    PROJECT_NAME: str = "FastAPI RabbitMQ Bridge"
    HANDLER_QUEUE: str = "handler-queue"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"

    LOG_LEVEL: LogLevel = "INFO"
    LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


settings = Settings()


def setup_logging() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
        force=True,
    )
