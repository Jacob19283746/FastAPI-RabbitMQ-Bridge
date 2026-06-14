from pydantic import BaseModel

class PushQueueResponse(BaseModel):
    status_code: int
    message: str
    data: dict

class HealthCheckResponse(BaseModel):
    status_code: int
    name_service: str