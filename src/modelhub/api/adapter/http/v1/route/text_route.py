from fastapi import APIRouter

from modelhub.api.adapter.http.v1.model.request.text_request import TextRequest

text_route = APIRouter()


@text_route.post(
    "/text",
    response_model=TextRequest,
    response_model_exclude_none=True,
    status_code=200
)
def text(text_request_body: TextRequest):
    return text_request_body