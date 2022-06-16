"""
Provider for AWS DynamoDB
"""

from typing import Any

import boto3
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table
from mypy_boto3_dynamodb.type_defs import PutItemOutputTypeDef

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.decorators.exponential_backoff import DecoratorExponentialBackoff


# pylint: disable=R0903
class ProviderDynamoDb:
    """
    Provider for AWS DynamoDB
    :param __ddb_resource: DynamoDB boto3 resource
    :type __ddb_resource: DynamoDBServiceResource
    :param __ddb_table: DynamoDB table boto3 resource
    :type __ddb_table: Table
    """

    def __init__(
        self,
        table_name: str,
        request_context: RequestContext,
        environ_context: EnvironmentContext,
    ) -> None:
        """
        Constructor
        :param table_name: Name of the DDB table
        :type table_name: str
        """

        LOGGER.logger.debug("Creating DynamoDB provider")

        self.__request_context = request_context
        self.__environ_context = environ_context

        self.__ddb_resource: DynamoDBServiceResource = boto3.resource(
            service_name="dynamodb",
            region_name=self.__environ_context.cloud_region_primary,
            endpoint_url=self.__environ_context.cloud_provider_api_endpoint_url,
        )

        self.__ddb_table: Table = self.__ddb_resource.Table(table_name)

    @property
    def ddb_table(self):
        """
        Get the ddb_table
        """

        return self.__ddb_table

    @DecoratorExponentialBackoff.retry(Exception)
    def put_item(self, item: Any) -> PutItemOutputTypeDef:
        """
        Insert new row in the DDB table
        :param item: The row attributes to be inserted
        :type item: Any
        """

        LOGGER.logger.debug(
            f"Inserting new item in table {self.__ddb_table.table_name}"
        )

        return self.__ddb_table.put_item(Item=item)
