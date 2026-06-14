import pytest


@pytest.mark.asyncio
async def test_get_enqueues_normalized_params(client, mock_rabbitmq):
    response = await client.get(
        "/",
        params={
            "phone_number": "79000000000",
            "message_text": "Hello World!",
            "custom_field": "value",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "status_code": 201,
        "message": "Successfully submitted parameters to the queue",
        "data": {
            "phone_number": "79000000000",
            "message_text": "Hello World!",
            "custom_field": "value",
        },
    }


@pytest.mark.asyncio
async def test_get_returns_400_without_params(client, mock_rabbitmq):
    response = await client.get("/")
    assert response.status_code == 400
