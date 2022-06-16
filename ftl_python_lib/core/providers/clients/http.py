"""
Provider for HTTP
"""

from typing import Optional
from typing import Union

import requests

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.typings.iso20022.received_message import TypeReceivedMessage
from ftl_python_lib.typings.iso20022.received_message import TypeReceivedMessageOut
from ftl_python_lib.typings.iso20022.received_message import TypeReceivedMessageProc
from ftl_python_lib.utils.mime import mime_json
from ftl_python_lib.utils.mime import mime_xml


class ProviderHttpInternal:
    """
    Provider for HTTP requests which happen internally (in the cluster)
    :param __request_context: Request context
    :type __request_context: RequestContext
    :param __environ_context: Environment context
    :type __environ_context: EnvironmentContext
    """

    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        self.__request_context: RequestContext = request_context
        self.__environ_context: EnvironmentContext = environ_context

        self.__session = requests.Session()

    def __clean_dict(self, src: dict) -> dict:
        if src is None:
            return {}

        for key, val in src.items():
            if val is None:
                del src[key]

        return src

    def __protocol(self, url: str) -> str:
        if "https://" in url or "http://" in url:
            return url
        return f"http://{url}"

    def content_type(self, data: Union[str, bytes, dict]) -> str:
        if isinstance(
            data,
            (
                dict,
                TypeReceivedMessage,
                TypeReceivedMessageOut,
                TypeReceivedMessageProc,
            ),
        ):
            return mime_json()

        return mime_xml()

    def post(
        self,
        url: str,
        data: Union[str, bytes, dict],
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ):
        if headers is None:
            headers = {}
        if params is None:
            params = {}
        if headers.get("Content-Type") is None:
            headers["Content-Type"] = self.content_type(data=data)

        headers = self.__clean_dict(src=headers)
        params = self.__clean_dict(src=params)
        url_ = self.__protocol(url=url)

        request = requests.Request(
            method="POST", url=url_, headers=headers, data=data, params=params
        )
        prepped = request.prepare()

        return self.__session.send(request=prepped)

    def get(
        self, url: str, headers: Optional[dict] = None, params: Optional[dict] = None
    ):
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        headers = self.__clean_dict(src=headers)
        params = self.__clean_dict(src=params)
        url_ = self.__protocol(url=url)

        request = requests.Request(
            method="GET", url=url_, headers=headers, params=params
        )
        prepped = request.prepare()

        return self.__session.send(request=prepped)
