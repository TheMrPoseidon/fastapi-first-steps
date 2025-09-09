from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_health() -> JSONResponse:
    return JSONResponse(status_code=200, content={"status": "healthy"})
