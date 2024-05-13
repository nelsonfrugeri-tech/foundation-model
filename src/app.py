import uvicorn
import time
import json
import os

from dotenv import load_dotenv

from fastapi import FastAPI, Request
from hub.api.adapter.http.v1.handle.generate_handle import router

from hub.api.adapter.log.log_http import LogHTTP

from hub.api.adapter.http.v1.handle.exception_handle import bad_request_exception

from hub.api.adapter.http.v1.model.exception.bad_request_exception import (
    BadRequestException,
)

from datadog_api_client.v2 import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


load_dotenv()

fast_api = FastAPI(title="modelhub-api", description="ModelHub API")


def add_middleware(fast_api: FastAPI) -> None:
    fast_api.add_middleware(LogHTTP)


def add_exception_handlers(fast_api) -> None:
    fast_api.add_exception_handler(BadRequestException, bad_request_exception)


def api():
    
    fast_api.include_router(router=router())

    add_exception_handlers(fast_api)

    add_middleware(fast_api)

    return fast_api


if __name__ == "__main__":
    uvicorn.run(
        api(), 
        host="0.0.0.0", 
        port=8080,
    )
