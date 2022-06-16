"""
Base exception
To be inherited by upper class exception
"""

from typing import Any
from typing import Dict
from typing import Optional

from flask import Response
from flask import make_response


class ExceptionBase(Exception):
    """
    Base exception class
    Each new custom exception should inherit this class
    :param __status_code: HTTP status code
    :type __status_code: Optional[int]
    :param __request_id: ID of the request
    :type __request_id: Optional[str]
    :param __message: Error message
    :type __message: str
    :param __headers: HTTP headers
    :type __headers: Optional[Dict[str, Any]]
    """

    __status_code: int = 500
    __request_id: str = "N/A"

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        headers: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> None:
        """
        Constructor
        :param request_id: Id of the request
        :type request_id: str
        :param message: Error message
        :type message: str
        :param status_code: HTTP status code
        :type status_code: Optional[int]
        :param headers: HTTP headers
        :type headers: Optional[Dict[str, Any]]
        """

        self.__message = message

        if request_id is not None:
            self.__request_id = request_id

        if status_code is not None:
            self.__status_code = status_code
        if status_code is not None:
            self.__headers = headers

        super().__init__()

    def __str__(self) -> str:
        """
        Default str conversion
        """

        err: str = f"""Request ID: {self.__request_id}
        {self.__message}
        """

        return err

    def response(self) -> Response:
        """
        Create Flask HTTP response
        """

        resp: Response = make_response(
            {
                "status": "Rejected",
                "message": self.__message,
                "request_id": self.__request_id,
            },
            self.__status_code,
        )

        if self.__headers is not None:
            resp.headers = self.__headers

        return resp
