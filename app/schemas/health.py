from pydantic import BaseModel


class HealthStatus(BaseModel):
    status_code: int = 200
    message: str = "Running"
