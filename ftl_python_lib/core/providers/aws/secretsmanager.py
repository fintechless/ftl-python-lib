"""
Provider for AWS SecretsManager
"""

import json

import boto3
import botocore.exceptions

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.decorators.exponential_backoff import DecoratorExponentialBackoff


# pylint: disable=R0903
class ProviderSecretsManager:
    """
    Provider for AWS SecretsManager
    :param __secretsmanager_resource: SecretsManager boto3 resource
    :type __secretsmanager_resource
    """

    __secretsmanager_resource = boto3.client("secretsmanager", region_name="us-east-1")

    def __init__(self, environ_context: EnvironmentContext) -> None:
        """
        Constructor
        :param secretsmanager_name: Name of the SecretManager
        :type secretsmanager_name: str
        """

        LOGGER.logger.debug("Creating SecretManager provider")

        self.__environ_context = environ_context
        self.__secretsmanager_resource = boto3.client(
            "secretsmanager", region_name=self.__environ_context.active_region
        )
        self.__secretsmanager_name: str = self.__environ_context.runtime_secretsmanager

    @DecoratorExponentialBackoff.retry(Exception)
    def get_value(self, secretsmanager_name: str = None):
        """
        Get object value
        """

        try:
            if secretsmanager_name is not None:
                self.__secretsmanager_name: str = secretsmanager_name
            LOGGER.logger.debug(
                f"Retrieving value: secretsmanager: {self.__secretsmanager_name}"
            )

            response = self.__secretsmanager_resource.get_secret_value(
                SecretId=self.__secretsmanager_name
            )
            LOGGER.logger.debug(
                f"Retrieved value: secretsmanager: {self.__secretsmanager_name}"
            )

            return json.loads(response["SecretString"])
        except botocore.exceptions.ClientError as exc:
            if exc.response.get("Error").get("Code") == "NoSuchKey":
                LOGGER.logger.error(
                    f"NoSuchKey! Could not retrieve value: secretsmanager: {self.__secretsmanager_name}"
                )
                LOGGER.logger.error(
                    f"Returning empty body for value: secretsmanager: {self.__secretsmanager_name}"
                )

                return b""

            raise exc

    @DecoratorExponentialBackoff.retry(Exception)
    def put_value(self, database_secrets, secretsmanager_name: str = None):
        """
        Get object value
        """

        try:
            if secretsmanager_name is not None:
                self.__secretsmanager_name: str = secretsmanager_name
            LOGGER.logger.debug(
                f"Save value: secretsmanager: {self.__secretsmanager_name}"
            )

            response = self.__secretsmanager_resource.put_secret_value(
                SecretId=self.__secretsmanager_name,
                SecretString=json.dumps(database_secrets),
            )

            LOGGER.logger.debug(
                f"Save value: secretsmanager: {self.__secretsmanager_name}"
            )

            return response
        except botocore.exceptions.ClientError as exc:
            if exc.response.get("Error").get("Code") == "NoSuchKey":
                LOGGER.logger.error(
                    f"NoSuchKey! Could not retrieve value: secretsmanager: {self.__secretsmanager_name}"
                )
                LOGGER.logger.error(
                    f"Returning empty body for value: secretsmanager: {self.__secretsmanager_name}"
                )

                return b""

            raise exc
