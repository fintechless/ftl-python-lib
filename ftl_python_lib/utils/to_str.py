"""
Utilities for converting data types to str (string)
"""

from typing import Optional
from typing import Union

from ftl_python_lib.core.log import LOGGER


def bytes_to_str(
    src: Union[bytes, str], encoding: Optional[str] = "utf-8"
) -> Optional[str]:
    """
    Convert bytes to string
    :param src: Source data
    :type src: bytes
    :param encoding: Result's encoding
    :type encoding: str
    """

    if src is None:
        LOGGER.logger.warning("Empty bytes will not be converted to string")

        return None
    if isinstance(src, str):
        LOGGER.logger.warning("Source data is already a string")

        return str

    LOGGER.logger.debug("Converting bytes to string")

    return src.decode(encoding=encoding)
