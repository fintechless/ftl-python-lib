import json
from typing import Union

from ftl_python_lib.constants.microservices import ConstantsMictoservicesHttp
from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.providers.clients.http import ProviderHttpInternal


class MircoserviceMsaRmqInResponse:
    """ """

    def __init__(
        self,
        request_id: str,
        status: str,
        headers: dict,
        status_code: int,
    ) -> None:
        self.__request_id = request_id
        self.__status = status

        self.__headers = headers
        self.__status_code = status_code

    @property
    def request_id(self) -> str:
        return self.__request_id

    @property
    def status(self) -> str:
        return self.__status

    @property
    def _headers(self) -> dict:
        return self.__headers

    @property
    def _status_code(self) -> int:
        return self.__status_code


class MicroserviceMsaRmqIn:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        self.__request_context = request_context
        self.__environ_context = environ_context

        self.__http = ProviderHttpInternal(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )
        self.__url = ConstantsMictoservicesHttp.MSA_RMQ_IN.value

    def post(
        self, data: Union[str, dict], headers: dict
    ) -> MircoserviceMsaRmqInResponse:
        resp = self.__http.post(url=self.__url, headers=headers, params={}, data=data)
        resp_json: dict = json.loads(resp.text)

        request_id: str = resp_json.get("request_id")
        status: str = resp_json.get("status")

        return MircoserviceMsaRmqInResponse(
            request_id=request_id,
            status=status,
            status_code=resp.status_code,
            headers=resp.headers,
        )
