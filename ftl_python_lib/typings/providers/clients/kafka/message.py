"""
Kafka message type definitions
"""

import json
from typing import Union

from ftl_python_lib.typings.providers.aws.s3object import TypeS3Object


class TypeClientsKafkaMessage(dict):
    """
    Kafka message custom type definition -- inherits dict type
    """

    @property
    def s3(self) -> TypeS3Object:
        """
        Get s3 value
        """

        __s3: dict = self.get("s3")

        return TypeS3Object(**__s3)

    @property
    def xmlj(self) -> dict:
        """
        Get XML value
        """

        __xmlj: Union[dict, str] = self.get("xmlj")

        if isinstance(__xmlj, str):
            return json.loads(__xmlj)

        return __xmlj

    @property
    def xmlo(self) -> str:
        """
        Get XML value
        """

        return self.get("xmlo")

    @property
    def request_id(self) -> str:
        """
        Get request_id value
        """

        return self.get("request_id")

    @property
    def requested_at(self) -> str:
        """
        Get timestamp value
        """

        return self.get("requested_at")

    @property
    def message_type(self) -> str:
        """
        Get message_type value
        """

        return self.get("message_type")

    @property
    def transaction_id(self) -> str:
        """
        Get transaction_id value
        """

        return self.get("transaction_id")
