from fastapi import APIRouter

from src.config.manager import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return {"status": "ok", "service": settings.app_name, "market": settings.market}
