import json
import logging

import aio_pika
from aio_pika import DeliveryMode

from app.handler import HandlerPayload
from app.settings import settings

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    def __init__(self, url: str, queue_name: str) -> None:
        self._url = url
        self.queue_name = queue_name
        self._connection: aio_pika.RobustConnection | None = None
        self._channel: aio_pika.Channel | None = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        await self._channel.declare_queue(self.queue_name, durable=True)
        logger.info("Connected to RabbitMQ, queue=%s", self.queue_name)

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()

    async def publish(self, payload: HandlerPayload) -> None:
        if self._channel is None:
            raise RuntimeError("RabbitMQ channel is not initialized")

        body = json.dumps(payload.root, ensure_ascii=False).encode("utf-8")
        await self._channel.default_exchange.publish(
            aio_pika.Message(
                body=body,
                content_type="application/json",
                delivery_mode=DeliveryMode.PERSISTENT,
            ),
            routing_key=self.queue_name,
        )
        logger.info("Published message to queue=%s keys=%s", self.queue_name, list(payload.root))


publisher = RabbitMQPublisher(settings.RABBITMQ_URL, settings.HANDLER_QUEUE)
