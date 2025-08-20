from fastapi import APIRouter, status

from ..schemas.health import HealthStatus

router = APIRouter(
    prefix="/health",
    tags=['health'],
)

@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_health():
    return HealthStatus()