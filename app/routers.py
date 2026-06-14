import json

from fastapi import APIRouter, Request, HTTPException

from app.services.params_normalizer import normalize_query_params
from app.services.rabbit_mq import rabbitmq_client
from app.schemas import PushQueueResponse, HealthCheckResponse

router = APIRouter(tags=["bridge-rabbit-queue"])

QUERY_EXAMPLES = [
    {
        "in": "query",
        "name": "phone_number",
        "schema": {"type": "string"},
        "required": False,
        "description": "Номер телефона",
        "example": "79000000000",
    },
    {
        "in": "query",
        "name": "name",
        "schema": {"type": "string"},
        "required": False,
        "description": "ФИО",
        "example": "Иванов Иван Иванович",
    },
    {
        "in": "query",
        "name": "message_text",
        "schema": {"type": "string"},
        "required": False,
        "description": "Сообщение",
        "example": "Hello World!",
    },
]

@router.get(
    "/",
    summary = "Отправить query-параметры в RabbitMQ",
    description = (
        f"Принимает **любые** query-параметры, нормализует и публикует"
        f"в очередь RabbitMQ.\n\n"
        "Один ключ в URL — строка в JSON; повтор того же ключа — массив строк. "
        "Параметры в Swagger ниже — только примеры, в URL можно передать любые ключи."
    ),
    openapi_extra={"parameters": QUERY_EXAMPLES}
)
async def publish_message(request: Request) -> PushQueueResponse:
    normalize_params =  await normalize_query_params(
        items=request.query_params.multi_items()
    )
    if not normalize_params:
        raise HTTPException(
            status_code=400,
            detail="Нужен хотя бы один query-параметр с непустым именем.",
        )
    result_published_msg = await rabbitmq_client.push_message(
        message=json.dumps(normalize_params, ensure_ascii=True).encode("utf-8")
    )
    if not result_published_msg:
        raise HTTPException(
            status_code=502,
            detail="Произошла ошибка при публикации сообщения в очередь RabbitMQ"
        )
    return PushQueueResponse(
        status_code=201,
        message="Successfully submitted parameters to the queue",
        data=normalize_params,
    )


@router.get("/health", summary="Проверка работоспособности сервиса")
async def health_check():
    if not rabbitmq_client.connection or rabbitmq_client.connection.is_closed:
        raise HTTPException(
            status_code=503,
            detail="RabbitMQ connection is not available"
        )

    return HealthCheckResponse(
        status_code=201,
        name_service="rabbit-mq-bridge"
    )