"""
Utility for working with datetime
"""

import datetime
from typing import Optional
from typing import Union

import pendulum
from pendulum import DateTime

from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.utils.timezone import UtilsTimezone


class UtilsDatetime:
    """
    Utility for working with datetime
    :param __timezone: Name of the timezone
    :type __timezone: Optional[Union[str, datetime.tzinfo]]
    :param __now: Current timestamp when the class was constructed
    :type __now: DateTime
    """

    def __init__(
        self,
        timezone: Optional[Union[str, datetime.tzinfo]] = None,
        from_source: Optional[Union[str, datetime.datetime]] = None,
    ) -> None:
        """
        Constructor
        :param timezone: Which timezone to use for datetime generation
        :type timezone: Optional[Union[str, datetime.tzinfo]]
        :param from_source: Generate current timestamp from a source
        :type from_source: Optional[Union[str, datetime.datetime]]
        """

        if timezone is not None:
            self.__timezone = timezone
        else:
            self.__timezone = UtilsTimezone().timezone

        LOGGER.logger.debug(
            f"Initializing datetime w/ pendulum. Timezone is {self.__timezone}"
        )

        self.__now = pendulum.now(tz=self.__timezone)

        if from_source is not None:
            if isinstance(from_source, str):
                self.__now = pendulum.parse(from_source)
            if isinstance(from_source, datetime.datetime):
                self.__now = pendulum.instance(from_source)
            self.__timezone = self.__now.timezone_name

    @property
    def now(self) -> DateTime:
        """
        Get current timestamp as DateTime or the timestamp parsed from `from_source` during instantiation
        """

        return self.__now

    @property
    def now_utc(self) -> DateTime:
        """
        Get current timestamp as DateTime or the timestamp parsed from `from_source` during instantiation
        """

        return self.__now.utcnow()

    @property
    def now_isoformat(self) -> str:
        """
        Get current UTC timestamp as str in ISO format
        """

        return self.__now.to_iso8601_string()

    @property
    def now_utc_isoformat(self) -> str:
        """
        Get current TC timestamp as str in ISO format
        """

        return self.__now.utcnow().to_iso8601_string()
