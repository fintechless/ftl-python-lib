"""
Utilities for converting data types to bytes (array)
"""

from typing import Optional

from ftl_python_lib.core.log import LOGGER


class UtilsConversionsToBytes:
    """
    Convert various data types to bytes
    """

    @staticmethod
    def str_to_bytes(src: str) -> Optional[bytes]:
        """
        Convert bytes to string
        :param src: Source data
        :type src: str
        :param encoding: Result's encoding
        :type encoding: bytes
        """

        if src is None:
            LOGGER.logger.warning("Empty str will not be converted to bytes")

            return None

        LOGGER.logger.debug("Converting string to bytes")

        return src.encode()
