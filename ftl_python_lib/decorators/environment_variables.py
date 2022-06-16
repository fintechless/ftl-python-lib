"""
Decorator for checking required environment variables
"""

import os
from functools import wraps
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from flask import session

from ftl_python_lib.core.context.request import REQUEST_CONTEXT_SESSION
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.exceptions.server_container_misconfigured_exception import ExceptionContainerMisconfigured
from ftl_python_lib.core.log import LOGGER


class DecoratorEnvironmentVariables:
    """
    A decorator for checking if the required
    environment variables are present
    """

    @staticmethod
    def required(
        request_context: Optional[RequestContext] = None,
        variables: Optional[Union[List[str], Tuple[str]]] = None,
    ):
        """
        :param request_context: The request id
        :type request_context: Optional[RequestContext]
        :param variables: Names of the environment variables to be checked
        :type variables: Optional[Union[List[str], Tuple[str]]]
        """

        def decorator_required(func):
            @wraps(func)
            def f_required(*args, **kwargs):
                if variables is None:
                    return func(*args, **kwargs)

                _missing: list[str] = []
                _request_context: RequestContext = request_context

                for variable in variables:
                    if os.environ.get(variable) is None:
                        _message: str = f"Missing environment variable `{variable}`"

                        LOGGER.logger.error(_message)

                        if _request_context is None:
                            _request_context = session.get(REQUEST_CONTEXT_SESSION)

                        _missing.append(variable)

                if len(_missing) != 0:
                    raise ExceptionContainerMisconfigured(
                        message=f"The following required environment variables are missing: `{','.join(_missing)}`",
                        request_context=_request_context,
                    )

                return func(*args, **kwargs)

            return f_required

        return decorator_required
