"""
Provider for AWS SecretsManager
"""

import json

import boto3
import botocore.exceptions

from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.decorators.exponential_backoff import DecoratorExponentialBackoff


# pylint: disable=R0903
class ProviderSecretsManagerEnviron:
    """
    Provider for AWS SecretsManager & Environment Congext
    :param __secretsmanager_resource: SecretsManager boto3 resource
    :type __secretsmanager_resource
    """

    def __init__(self, environ_context) -> None:
        """
        Constructor
        :param secretsmanager_name: Name of the SecretManager
        :type secretsmanager_name: str
        """

        LOGGER.logger.debug("Creating SecretManager provider")
        self.__secretsmanager_resource = boto3.client("secretsmanager", region_name=environ_context.cloud_region_primary)

        self.__environment_context_secret_name: str = environ_context.environment_context_secret_name

    @DecoratorExponentialBackoff.retry(Exception)
    def get_value(self):
        """
        Get object value
        """

        try:
            secretsmanager_name: str = self.__environment_context_secret_name
            LOGGER.logger.debug(f"Retrieving value: secretsmanager: {secretsmanager_name}")

            response = self.__secretsmanager_resource.get_secret_value(SecretId=secretsmanager_name)
            LOGGER.logger.debug(f"Retrieved value: secretsmanager: {secretsmanager_name}")

            return json.loads(response["SecretString"])
        except botocore.exceptions.ClientError as exc:
            if exc.response.get("Error").get("Code") == "NoSuchKey":
                LOGGER.logger.error(
                    f"NoSuchKey! Could not retrieve value: secretsmanager: {secretsmanager_name}"
                )
                LOGGER.logger.error(
                    f"Returning empty body for value: secretsmanager: {secretsmanager_name}"
                )

                return b""

            raise exc
