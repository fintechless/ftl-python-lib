"""
Liquidity model
Database: DynamoDB
"""

import uuid

from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.type_defs import QueryOutputTypeDef

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.core.providers.aws.dynamodb import ProviderDynamoDb
from ftl_python_lib.typings.models.liquidity import TypeLiquidity
from ftl_python_lib.utils.timedate import UtilsDatetime


class ModelLiquidity:
    """
    Liquidity model class
    :param __table_name: Name of the table
    :type __table_name: str
    :param __provider_ddb: DynamoDB provider
    :type __provider_ddb: ProviderDynamoDb
    :param __request_context: Context about the request
    :type __request_context: RequestContext
    """

    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        :param table_name: Name of the table
        :type table_name: str
        :param request_context: Context about the request
        :type request_context: RequestContext
        """

        LOGGER.logger.debug("Creating model for Liquidity")
        LOGGER.logger.debug(f"FTL Request ID: {request_context.request_id}")

        self.__request_context = request_context
        self.__environ_context = environ_context

        self.__table_name = f"ftl-api-liquidity-{self.__environ_context.environment}"

        LOGGER.logger.debug(f"Model table name is {self.__table_name}")

        self.__provider_ddb: ProviderDynamoDb = ProviderDynamoDb(
            table_name=self.__table_name,
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )

    def balance(self, user_id: str, deployment_id: str) -> TypeLiquidity:
        """
        Get current balance for user_id
        """

        results: QueryOutputTypeDef = self.__provider_ddb.ddb_table.query(
            IndexName="gsi-userid-balance",
            KeyConditionExpression=Key("user_id").eq(user_id)
            & Key("deployment_id").eq(deployment_id),
            ScanIndexForward=True,  # ORDER BY REVERSE
        )

        if results.get("Count") > 0:
            return TypeLiquidity(results.get("Items").pop())

        return TypeLiquidity(balance=0)

    def liquidity(
        self,
        deployment_id: str,
        entity_id: str,
        user_id: str,
        currency: str,
        amount: int,
    ) -> TypeLiquidity:
        """
        Add new liquidity
        """

        LOGGER.logger.debug("Adding new liquidity")

        balance: int = 0
        __balance: int = self.balance(
            user_id=user_id, deployment_id=deployment_id
        ).balance
        if __balance + (amount) >= 0:
            balance = __balance + (amount)

        item: TypeLiquidity = TypeLiquidity(
            id=str(uuid.uuid4()),
            created_at=UtilsDatetime().now_isoformat,
            request_id=self.__request_context.request_id,
            requested_at=self.__request_context.requested_at_isoformat,
            deployment_id=deployment_id,
            entity_id=entity_id,
            user_id=user_id,
            currency=currency,
            amount=amount,
            balance=balance,
        )

        self.__provider_ddb.put_item(item=item)

        LOGGER.logger.debug("Added new liquidity")

        return item
