"""
Decorator for exponential backoff
"""

import time
from functools import wraps
from typing import Tuple
from typing import Union

from ftl_python_lib.core.log import LOGGER


# pylint: disable=R0903
# too-few-public-methods
class DecoratorExponentialBackoff:
    """
    A decorator for triggering an exponential backoff
    when specific Exceptions are catched
    """

    @staticmethod
    def retry(
        exception: Union[Exception, Tuple[Exception]],
        tries: int = 4,
        delay: int = 3,
        backoff: int = 2,
    ):
        """
        :param exception: the exception to check
        :type exception: Union[Exception, Tuple[Exception]]
        :param tries: number of times to try (not retry) before giving up
        :type tries: int
        :param delay: initial delay between retries in seconds
        :type delay: int
        :param backoff: backoff multiplier e.g. value of 2 will double the delay
            each retry
        :type backoff: int
        :param logger: logger to use. If None, print
        :type logger: logging.Logger instance
        """

        def decorator_retry(func):
            @wraps(func)
            def f_retry(*args, **kwargs):
                # mtries, mdelay = tries, delay
                mtries: int = tries
                mdelay: int = delay

                while mtries > 1:
                    try:
                        return func(*args, **kwargs)
                    except exception as exc:
                        message: str = f"An exception was catched: {str(exc)} ... Retrying in {mdelay} seconds"
                        LOGGER.logger.error(message)

                        time.sleep(mdelay)

                        mtries -= 1
                        mdelay *= backoff

                return func(*args, **kwargs)

            return f_retry

        return decorator_retry
