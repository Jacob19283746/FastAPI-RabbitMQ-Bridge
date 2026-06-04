from collections.abc import Iterator
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> Iterator[TestClient]:
    from app.rabbit import publisher
    from main import app

    with (
        patch.object(publisher, "connect", new_callable=AsyncMock),
        patch.object(publisher, "close", new_callable=AsyncMock),
        patch.object(publisher, "publish", new_callable=AsyncMock) as publish_mock,
    ):
        publish_mock.return_value = None
        with TestClient(app) as test_client:
            yield test_client
