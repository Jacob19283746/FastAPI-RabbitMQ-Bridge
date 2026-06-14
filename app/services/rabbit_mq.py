import os
import datetime

import aio_pika

from app.logger import logger


class RabbitMQClient:
    """Клиент для работы с очередью сообщений

    Методы:
      - Подключение к серверу и создание канала connect()
      - Закрытие соединения close_connecton()
      - Добавление сообщения в очередь push_messagge()
    """
    def __init__(self, url_rabbitmq: str, queue_name: str, publisher_confirms: bool = True) -> None:
        self.url_rabbitmq = url_rabbitmq
        self.queue_name = queue_name
        self.publisher_confirms = publisher_confirms
        self.connection = None
        self.channel = None


    async def connect(self) -> bool:
        try:
            if not self.url_rabbitmq:
                logger.warning('Не указан URL сервера')
                return False

            self.connection = await aio_pika.connect_robust(self.url_rabbitmq)
            self.channel = await self.connection.channel(publisher_confirms=self.publisher_confirms)
            queue = await self.channel.declare_queue(name=self.queue_name, durable=True)
            logger.info(f"Установлено соединение RabbitMQ, очередь: {queue}")
            return True

        except Exception as error:
            logger.exception(f"Непредвиденная ошибка подключения: {error}")
            return False

    async def close(self) -> bool:
        try:
            if self.channel and not self.channel.is_closed:
                await self.channel.close()

            if self.connection and not self.connection.is_closed:
                await self.connection.close()
                logger.info(f"Соединение RabbitMQ закрыто")
                return True

            logger.warning("Нет активных соединений для завершения")
            return True

        except Exception as error:
            logger.exception(f"Непредвиденная ошибка при закрытии соединения: {error}")
            return False

    async def push_message(self, message: bytes) -> bool:
        try:
            if not self.connection or not self.channel:
                logger.warning(f"RabbitMQ не подключен. Необходимо выполнить подключение connect()")
                return False

            result = await self.channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=message,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    timestamp=datetime.datetime.now()
                ),
                routing_key=self.queue_name,
                # timeout=0.01
            )
            logger.debug(result.name if result else None)
            logger.info(f"Отправлено сообщение в очередь {self.queue_name}")
            return True

        except Exception as error:
            logger.exception(f"Непредвиденная ошибка при отправке сообщения: {error}")
            return False


rabbitmq_client = RabbitMQClient(
    url_rabbitmq=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:"),
    queue_name=os.getenv("RABBITMQ_QUEUE", "fastapi_bridge"),
    publisher_confirms=False
)


if __name__ == '__main__':
    import asyncio

    async def run():
        await rabbitmq_client.connect()
        await rabbitmq_client.push_message(b"Hello World!")
        await rabbitmq_client.close()

    asyncio.run(run())
