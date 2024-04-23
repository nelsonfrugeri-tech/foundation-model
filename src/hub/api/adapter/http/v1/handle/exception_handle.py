from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status

from hub.api.adapter.http.v1.model.exception.bad_request_exception import (
    BadRequestException,
)
from hub.api.adapter.http.v1.model.response.error_response import ErrorResponse


async def bad_request_exception(request: Request, exception: BadRequestException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            ErrorResponse(
                code="ERROR_001", message=f"Bad Request", details=exception.get_params()
            )
        ),
    )
