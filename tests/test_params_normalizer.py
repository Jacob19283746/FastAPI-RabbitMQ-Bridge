import pytest

from app.services.params_normalizer import normalize_query_params


@pytest.mark.asyncio
async def test_normalize_trims_keys_and_values():
    items = [(" phone_number ", " 79000000000 "), ("message_text", " Hello ")]
    assert await normalize_query_params(items) == {
        "phone_number": "79000000000",
        "message_text": "Hello",
    }


@pytest.mark.asyncio
async def test_normalize_skips_empty_key():
    items = [("", "ignored"), ("valid", "ok")]
    assert await normalize_query_params(items) == {"valid": "ok"}


@pytest.mark.asyncio
async def test_normalize_null_params():
    items = []
    assert await normalize_query_params(items) == {}


@pytest.mark.asyncio
async def test_normalize_keeps_arbitrary_keys():
    items = [("order_id", "42"), ("status", "new")]
    assert await normalize_query_params(items) == {
        "order_id": "42",
        "status": "new",
    }


@pytest.mark.asyncio
async def test_normalize_merges_duplicate_keys_into_list():
    items = [("tag", "a"), ("tag", "b"), ("id", "1")]
    assert await normalize_query_params(items) == {
        "tag": ["a", "b"],
        "id": "1",
    }
