"""
Context for the HTTP request
Contains the id and timestamp and must be initialized before each request
"""

import uuid
from typing import Optional

from ftl_python_lib.core.context.headers import HeadersContext
from ftl_python_lib.utils.timedate import DateTime
from ftl_python_lib.utils.timedate import UtilsDatetime

REQUEST_CONTEXT_SESSION: str = "_request_context"


class RequestContext:
    """
    FTL Context about the HTTP request
    Contains the id and timestamp of the request
    :param __request_id: ID of the request
    :type __request_id: str
    :param __datetime: Date & time utils
    type __datetime: UtilsDatetime
    :param __transaction_id: Date & time utils
    type __transaction_id: UtilsDatetime
    """

    def __init__(
        self,
        headers_context: HeadersContext,
    ) -> None:
        self.__headers_context = headers_context

        self.__transaction_id = None
        self.__request_id: str = str(uuid.uuid4())
        self.__datetime: UtilsDatetime = UtilsDatetime()

    def reset_request_id(self) -> None:
        """
        Reset the request_id value
        """

        self.__request_id = str(uuid.uuid4())

    def reset_datetime(self) -> None:
        """
        Reset the datetime value
        """

        self.__datetime = UtilsDatetime()

    @property
    def request_id(self) -> str:
        """
        Return the request_id value
        """

        return self.__request_id

    @request_id.setter
    def request_id(self, request_id) -> None:
        """
        Set the request_id value
        """

        self.__request_id = request_id

    @property
    def requested_at_datetime(self) -> DateTime:
        """
        Return the requested_at value as DateTime
        """

        return self.__datetime.now

    @property
    def requested_at_isoformat(self) -> str:
        """
        Return the requested_at value as str in ISO format
        """

        return self.__datetime.now_isoformat

    @property
    def headers_context(self) -> HeadersContext:
        return self.__headers_context

    @property
    def transaction_id(self) -> Optional[str]:
        """
        Return the transaction_id value as str
        """

        if self.__transaction_id is not None:
            return self.__transaction_id

        return self.__headers_context.transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id: str) -> None:
        """
        Set transaction_id value
        """

        self.__transaction_id: str = transaction_id

    def to_dict(self) -> dict:
        """
        Class convertor to dict
        """

        return {
            "request_id": self.request_id,
            "requested_at_datetime": self.requested_at_datetime,
            "requested_at_isoformat": self.requested_at_isoformat,
            "transaction_id": self.transaction_id,
            "headers_context": self.headers_context,
        }
