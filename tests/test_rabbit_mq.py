import pytest

@pytest.mark.asyncio
async def test_rabbit_mq_connection(mock_rabbitmq):
    assert await mock_rabbitmq.connect()
    assert await mock_rabbitmq.close()


@pytest.mark.asyncio
async def test_publish_message_to_queue(mock_rabbitmq):
    assert await mock_rabbitmq.connect()
    assert await mock_rabbitmq.push_message(b"my_test_exchange")
    assert await mock_rabbitmq.close()