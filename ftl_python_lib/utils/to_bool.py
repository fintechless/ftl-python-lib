"""
Utilities for converting data types to bool (boolean)
"""

from ftl_python_lib.core.log import LOGGER


def str_to_bool(src: str) -> bool:
    LOGGER.logger.debug("Converting string to boolean")

    if src in ("y", "yes", "t", "true", "on", "1"):
        return True
    if src in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"Invalid truth value {src}")


class UtilsConversionsToBool:
    """
    Convert various data types to bool
    """

    @staticmethod
    def str_to_bool(src: str) -> bool:
        """
        Convert string to bool
        :param src: Source data
        :type src: str
        """

        LOGGER.logger.debug("Converting string to boolean")

        if src in ("y", "yes", "t", "true", "on", "1"):
            return True
        if src in ("n", "no", "f", "false", "off", "0"):
            return False
        raise ValueError(f"Invalid truth value {src}")
