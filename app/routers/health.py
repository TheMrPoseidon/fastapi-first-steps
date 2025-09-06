from fastapi import APIRouter, status
from fastapi.responses import Response


router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_health() -> Response:
    return Response(status_code=200, content="healthy")
