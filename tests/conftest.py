import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_rabbitmq(monkeypatch):
    class MockRabbitMQ:
        async def connect(self):
            return True

        async def close(self):
            return True

        async def push_message(self, message: bytes) -> bool:
            return True

    mock = MockRabbitMQ()
    monkeypatch.setattr("app.routers.rabbitmq_client", mock)
    return mock
