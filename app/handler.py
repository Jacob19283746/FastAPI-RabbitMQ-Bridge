from collections.abc import Iterable

from fastapi import HTTPException
from pydantic import BaseModel, Field, RootModel, ValidationError

from app.settings import settings

QueryValue = str | list[str]


class HandlerPayload(RootModel[dict[str, QueryValue]]):
    """Все query-параметры GET-запроса."""
    root: dict[str, QueryValue] = Field(default_factory=dict)


class EnqueueResponse(BaseModel):
    """Ответ после постановки сообщения в очередь."""
    status: str = "queued"
    queue: str
    data: dict[str, QueryValue]


def normalize_query_params(items: Iterable[tuple[str, str]]) -> dict[str, QueryValue]:
    """Обрезка пробелов; пустые имена отбрасываются; повтор ключа → список значений."""
    normalized: dict[str, QueryValue] = {}
    for key, value in items:
        clean_key = key.strip()
        if not clean_key:
            continue
        clean_value = value.strip()
        existing = normalized.get(clean_key)
        if existing is None:
            normalized[clean_key] = clean_value
        elif isinstance(existing, list):
            existing.append(clean_value)
        else:
            normalized[clean_key] = [existing, clean_value]
    return normalized


def build_payload(items: Iterable[tuple[str, str]]) -> HandlerPayload:
    """Сбор данных из запроса и их нормализация."""
    normalized = normalize_query_params(items)
    if not normalized:
        raise HTTPException(
            status_code=400,
            detail="Нужен хотя бы один query-параметр с непустым именем.",
        )
    try:
        return HandlerPayload(normalized)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc


def to_response(payload: HandlerPayload) -> EnqueueResponse:
    """Преобразование результата обработки к формату ответного JSON-объекта."""
    return EnqueueResponse(
        queue=settings.HANDLER_QUEUE,
        data=payload.root,
    )
