"""
AWS S3 object type definitions
"""

from typing import Union


class TypeS3Object:
    """
    AWS S3 object custom type definition -- inherits dict type
    """

    def __init__(self, bucket: str, key: str, body: Union[str, bytes, None]) -> None:
        self.__bucket = bucket
        self.__key = key
        self.__body = body

    @property
    def bucket(self) -> str:
        """
        Get object's bucket name
        """

        return self.__bucket

    @property
    def key(self) -> str:
        """
        Get object's key
        """

        return self.__key

    @property
    def body(self) -> Union[bytes, str, None]:
        """
        Get object's body (if present)
        """

        return self.__body
