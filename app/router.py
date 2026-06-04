from __future__ import annotations

from fastapi import APIRouter, Request

from app.handler import EnqueueResponse, build_payload, to_response
from app.rabbit import publisher
from app.settings import settings

router = APIRouter(tags=["bridge"])

_OPENAPI_QUERY_EXAMPLES = [
    {
        "in": "query",
        "name": "phone_number",
        "schema": {"type": "string"},
        "required": False,
        "description": "Пример: номер телефона",
        "example": "79000000000",
    },
    {
        "in": "query",
        "name": "name",
        "schema": {"type": "string"},
        "required": False,
        "description": "Пример: ФИО",
        "example": "Иванов Иван Иванович",
    },
    {
        "in": "query",
        "name": "message_text",
        "schema": {"type": "string"},
        "required": False,
        "description": "Пример: текст сообщения",
        "example": "Hello World!",
    },
]


@router.get(
    "/",
    response_model=EnqueueResponse,
    summary="Отправить query-параметры в RabbitMQ",
    description=(
        f"Принимает **любые** query-параметры, нормализует их и публикует JSON "
        f"в очередь `{settings.HANDLER_QUEUE}`.\n\n"
        "Один ключ в URL — строка в JSON; повтор того же ключа — массив строк. "
        "Параметры в Swagger ниже — только примеры, в URL можно передать любые ключи."
    ),
    openapi_extra={"parameters": _OPENAPI_QUERY_EXAMPLES},
)
async def handle_get(request: Request) -> EnqueueResponse:
    payload = build_payload(request.query_params.multi_items())
    await publisher.publish(payload)
    return to_response(payload)

