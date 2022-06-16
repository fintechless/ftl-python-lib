"""
Utility for working with timezones
"""
from datetime import datetime
from datetime import timezone
from datetime import tzinfo

from ftl_python_lib.core.log import LOGGER


def get_timezone() -> tzinfo:
    return datetime.now(timezone.utc).astimezone().tzinfo


class UtilsTimezone:
    """
    Utility for working with timezones
    :param __timezone: Timezone name
    :type __timezone: tzinfo
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        self.__timezone: tzinfo = datetime.now(timezone.utc).astimezone().tzinfo

        LOGGER.logger.debug(
            f"Initializing timezone. Current timezone is {self.__timezone}"
        )

    @property
    def timezone(self) -> tzinfo:
        """
        Get timezone
        """

        return self.__timezone
