import os
import time
import json

from dotenv import load_dotenv

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from datadog_api_client.v2 import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


class LogHTTP(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        try:
            super().__init__(app)

            load_dotenv()

            self.config = Configuration()            
            self.config.api_key['DD_API_KEY'] = os.getenv("DD_API_KEY")
            self.config.server_variables["site"] = "us5.datadoghq.com"
            
            self.logs = LogsApi(ApiClient(configuration=self.config))
        except Exception as exception:
            raise exception

    def dispatch(self, request: Request, call_next):
        try:
            start_time = time.time()

            response = call_next(request)

            self.log(request, response, start_time)

            return response
        except Exception as exception:
            raise exception

    def log(self, request: Request, response: Response, start_time: float):
        try:
            duration = time.time() - start_time

            body = HTTPLog(
                [
                    HTTPLogItem(
                        ddsource="Python",
                        ddtags="env:{}".format(os.getenv("DD_LOGGING_ENV")),
                        hostname="{}".format(os.getenv("DD_HOSTNAME")),
                        message= json.dumps(
                            {
                                "endpoint": request.url.path,
                                "method": request.method,
                                # "status": response.status_code,
                                "latency": duration
                            }
                        ),
                        service="foundation-model"                        
                    ),
                ]
            )

            self.logs.submit_log(content_encoding='gzip', body=body)
        except Exception as exception:
            raise exception