import uvicorn

from fastapi import FastAPI
from hub.api.adapter.http.v1.handle.generate_handle import router

from hub.api.adapter.http.v1.handle.exception_handle import bad_request_exception

from hub.api.adapter.http.v1.model.exception.bad_request_exception import (
    BadRequestException,
)


def add_exception_handlers(fast_api):
    fast_api.add_exception_handler(BadRequestException, bad_request_exception)


def api():
    fast_api = FastAPI(title="modelhub-api", description="ModelHub API")

    fast_api.include_router(router=router())

    add_exception_handlers(fast_api)

    return fast_api


if __name__ == "__main__":
    uvicorn.run(api(), host="0.0.0.0", port=8080)
