"""
Make HTTP calls to Mapping Microservice
"""

import json
from typing import List

from ftl_python_lib.constants.microservices import ConstantsMictoservicesHttp
from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.providers.clients.http import ProviderHttpInternal
from ftl_python_lib.models.sql.mapping import ModelMapping


class MircoserviceApiMappingResponse:
    """ """

    def __init__(
        self,
        request_id: str,
        status: str,
        data: list[ModelMapping],
        headers: dict,
        status_code: int,
    ) -> None:
        self.__request_id = request_id
        self.__status = status
        self.__data = data

        self.__headers = headers
        self.__status_code = status_code

    @property
    def request_id(self) -> str:
        return self.__request_id

    @property
    def status(self) -> str:
        return self.__status

    @property
    def data(self) -> list[ModelMapping]:
        return self.__data

    @property
    def _headers(self) -> dict:
        return self.__headers

    @property
    def _status_code(self) -> int:
        return self.__status_code


class MicroserviceApiMapping:
    """ """

    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        self.__request_context = request_context
        self.__environ_context = environ_context

        self.__http = ProviderHttpInternal(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )
        self.__url = ConstantsMictoservicesHttp.API_MAPPING.value

    def get(self, params: dict, headers: dict = None):
        resp = self.__http.get(url=self.__url, headers=headers, params=params)
        resp_json: dict = json.loads(resp.text)

        request_id: str = resp_json.get("request_id")
        status: str = resp_json.get("status")
        data: List[dict] = resp_json.get("data")

        return MircoserviceApiMappingResponse(
            request_id=request_id,
            status=status,
            data=[ModelMapping(**it) for it in data],
            headers=resp.headers,
            status_code=resp.status_code,
        )
