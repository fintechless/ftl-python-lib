"""
HTTP 500 Internal Server Exception -- Unexpected error
"""

from typing import Any
from typing import Dict
from typing import Optional

from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.exceptions.base_exception import ExceptionBase


class ExceptionUnexpectedError(ExceptionBase):
    """
    HTTP 500 Internal Server Exception -- Unexpected error
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

    def __init__(
        self,
        request_context: RequestContext,
        message: str,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Constructor
        :param request_context: Context about the request
        :type request_context: RequestContext
        :param message: Error message
        :type message: str
        :param status_code: HTTP status code
        :type status_code: int
        :param headers: HTTP headers
        :type headers: Optional[Dict[str, Any]]
        """

        super().__init__(
            message=message,
            status_code=self.__status_code,
            headers=headers,
            request_id=request_context.request_id,
        )
