import pytest

from app.services.rabbit_mq import rabbitmq_client

@pytest.mark.asyncio
async def test_rabbit_mq_connection():
    assert await rabbitmq_client.connect()
    assert await rabbitmq_client.close()


@pytest.mark.asyncio
async def test_publish_message_to_queue():
    assert await rabbitmq_client.connect()
    assert await rabbitmq_client.push_message(b"my_test_exchange")
    assert await rabbitmq_client.close()