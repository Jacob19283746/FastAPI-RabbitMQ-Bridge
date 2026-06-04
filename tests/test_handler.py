import pytest
from fastapi import HTTPException

from app.handler import (
    build_payload,
    normalize_query_params,
    to_response,
)


def test_normalize_trims_keys_and_values():
    items = [(" phone_number ", " 79000000000 "), ("message_text", " Hello ")]
    assert normalize_query_params(items) == {
        "phone_number": "79000000000",
        "message_text": "Hello",
    }


def test_normalize_skips_empty_key():
    items = [("", "ignored"), ("valid", "ok")]
    assert normalize_query_params(items) == {"valid": "ok"}


def test_normalize_keeps_arbitrary_keys():
    items = [("order_id", "42"), ("status", "new")]
    assert normalize_query_params(items) == {
        "order_id": "42",
        "status": "new",
    }


def test_normalize_merges_duplicate_keys_into_list():
    items = [("tag", "a"), ("tag", "b"), ("id", "1")]
    assert normalize_query_params(items) == {
        "tag": ["a", "b"],
        "id": "1",
    }


def test_build_payload_raises_when_empty():
    with pytest.raises(HTTPException) as exc_info:
        build_payload([("", "only-empty-key")])
    assert exc_info.value.status_code == 400


def test_build_payload_returns_normalized_data():
    payload = build_payload([(" phone ", " x ")])
    assert payload.root == {"phone": "x"}


def test_to_response_format():
    payload = build_payload([("phone_number", "79000000000")])
    response = to_response(payload)
    assert response.status == "queued"
    assert response.queue == "handler-queue"
    assert response.data == {"phone_number": "79000000000"}
