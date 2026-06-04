def test_get_enqueues_normalized_params(client):
    response = client.get(
        "/",
        params={
            "phone_number": "79000000000",
            "message_text": "Hello World!",
            "custom_field": "value",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "queued",
        "queue": "handler-queue",
        "data": {
            "phone_number": "79000000000",
            "message_text": "Hello World!",
            "custom_field": "value",
        },
    }


def test_get_returns_400_without_params(client):
    response = client.get("/")
    assert response.status_code == 400


def test_get_publishes_to_rabbitmq(client):
    from app.rabbit import publisher

    client.get("/", params={"id": "1"})

    publisher.publish.assert_awaited_once()
    payload = publisher.publish.await_args.args[0]
    assert payload.root == {"id": "1"}


def test_get_merges_duplicate_query_keys(client):
    response = client.get("/", params=[("tag", "a"), ("tag", "b"), ("id", "1")])

    assert response.status_code == 200
    assert response.json()["data"] == {"tag": ["a", "b"], "id": "1"}
