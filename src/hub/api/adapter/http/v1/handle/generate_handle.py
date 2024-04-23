from fastapi import APIRouter

from hub.api.adapter.http.v1.route.health_route import health_router
from hub.api.adapter.http.v1.route.text_route import text_route


def router():
    api_router = APIRouter()

    api_router.include_router(
        health_router, prefix="/v1/generate", tags=["health-router"]
    )
    api_router.include_router(text_route, prefix="/v1/generate", tags=["text-router"])

    return api_router
