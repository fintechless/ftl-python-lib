"""
Transaction model
Database: DynamoDB
"""

import datetime
import uuid

from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Key
from mypy_boto3_dynamodb.type_defs import QueryOutputTypeDef

from ftl_python_lib.constants.models.transaction import ConstantsTransactionStatus
from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.exceptions.server_unexpected_error_exception import ExceptionUnexpectedError
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.core.providers.aws.dynamodb import ProviderDynamoDb
from ftl_python_lib.models.sql.history_transaction import ModelHistoryTransaction
from ftl_python_lib.models_helper.history_transaction import HelperHistoryTransaction
from ftl_python_lib.typings.models.transaction import TypeTransaction
from ftl_python_lib.utils.timedate import UtilsDatetime
from ftl_python_lib.typings.iso20022.received_message import TypeReceivedMessage


class ModelTransaction:
    """
    Transaction model class
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

        LOGGER.logger.debug("Creating model for Transaction")
        LOGGER.logger.debug(f"FTL Request ID: {request_context.request_id}")

        self.__request_context = request_context
        self.__environ_context = environ_context

        self.__table_name = f"ftl-api-transaction-{self.__environ_context.environment}"

        LOGGER.logger.debug(f"Model table name is {self.__table_name}")

        self.__provider_ddb: ProviderDynamoDb = ProviderDynamoDb(
            table_name=self.__table_name,
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )

    def initiate(self) -> TypeTransaction:
        """
        Initiate transaction: insert new row with initiated status
        """

        _id: str = str(uuid.uuid4())
        created_at: str = UtilsDatetime().now_isoformat
        status: str = ConstantsTransactionStatus.INITIATED.value
        transaction_id: str = str(uuid.uuid4())

        LOGGER.logger.debug("Initiating transaction")
        LOGGER.logger.debug(f"\tID {_id}")
        LOGGER.logger.debug(f"\tCREATED AT {created_at}")
        LOGGER.logger.debug(f"\tSTATUS {status}")
        LOGGER.logger.debug(f"\tTRANSACTION ID {transaction_id}")

        item: TypeTransaction = TypeTransaction(
            id=_id,
            transaction_id=transaction_id,
            created_at=created_at,
            status=status,
            requested_at=self.__request_context.requested_at_isoformat,
        )

        if self.__environ_context.deployment_id is not None:
            item["deployment_id"] = self.__environ_context.deployment_id

        self.__provider_ddb.put_item(item=item)

        self.__request_context.transaction_id = transaction_id

        LOGGER.logger.debug("Transaction is now initiated")

        return item

    def latest(self) -> list[TypeTransaction]:
        """
        Latest transactions: retrieve the latest 50 transactions
        """

        status_released: str = ConstantsTransactionStatus.RELEASED.value
        status_rejected: str = ConstantsTransactionStatus.REJECTED.value
        status_notified: str = ConstantsTransactionStatus.NOTIFIED.value
        status_canceled: str = ConstantsTransactionStatus.CANCELED.value

        result: QueryOutputTypeDef = self.__provider_ddb.ddb_table.scan(
            FilterExpression=Attr("status").is_in(
                [status_released, status_rejected, status_notified, status_canceled]
            )
            & Attr("retrieved_at").not_exists()
        )

        result_count: int = result.get("Count")
        LOGGER.logger.debug(f"Retrieve the latest `{result_count}` transactions")

        return result.get("Items")

    def receive(
        self,
        storage_path: str,
        message_type: str,
        ht_response_code: str,
        ht_response_message: str,
        currency: str,
        amount: str,
    ) -> TypeTransaction:
        """
        Receive transaction: insert new row with received status
        :param storage_path: Path where the XML message is stored
        :type storage_path: str
        :param message_type: Type of the XML message
        :type message_type: str
        """

        _id: str = str(uuid.uuid4())
        created_at: str = UtilsDatetime().now_isoformat
        status: str = ConstantsTransactionStatus.RECEIVED.value

        LOGGER.logger.debug("Receiving transaction")
        LOGGER.logger.debug(f"\tID {_id}")
        LOGGER.logger.debug(f"\tCREATED AT {created_at}")
        LOGGER.logger.debug(f"\tSTATUS {status}")
        LOGGER.logger.debug(f"\tTRANSACTION ID {self.__request_context.transaction_id}")

        item: TypeTransaction = TypeTransaction(
            id=_id,
            transaction_id=self.__request_context.transaction_id,
            created_at=created_at,
            status=status,
            requested_at=self.__request_context.requested_at_isoformat,
            storage_path=storage_path,
            message_type=message_type,
        )

        if self.__environ_context.deployment_id is not None:
            item["deployment_id"] = self.__environ_context.deployment_id

        self.__provider_ddb.put_item(item=item)

        LOGGER.logger.debug("Transaction is now received")

        HelperHistoryTransaction(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        ).create(
            history_transaction_new=ModelHistoryTransaction(
                request_id=self.__request_context.request_id,
                requested_at=self.__request_context.requested_at_utc_isoformat,
                transaction_id=self.__request_context.transaction_id,
                status=status,
                message_type=message_type,
                response_code=ht_response_code,
                response_message=ht_response_message,
                currency=currency,
                amount=amount,
                storage_path=storage_path,
            ),
            owner_member_id=self.__request_context.default_owner_id,
        )

        return item

    def reject(
        self,
        storage_path: str,
        message_type: str,
        ht_response_code: str,
        ht_response_message: str,
        currency: str,
        amount: str,
    ) -> TypeTransaction:
        """
        Reject transaction: insert new row with rejected status
        :param storage_path: Path where the XML message is stored
        :type storage_path: str
        :param message_type: Type of the XML message
        :type message_type: str
        """

        _id: str = str(uuid.uuid4())
        created_at: str = UtilsDatetime().now_isoformat
        status: str = ConstantsTransactionStatus.REJECTED.value

        LOGGER.logger.debug("Rejecting transaction")
        LOGGER.logger.debug(f"\tID {_id}")
        LOGGER.logger.debug(f"\tCREATED AT {created_at}")
        LOGGER.logger.debug(f"\tSTATUS {status}")
        LOGGER.logger.debug(f"\tTRANSACTION ID {self.__request_context.transaction_id}")

        item: TypeTransaction = TypeTransaction(
            id=_id,
            transaction_id=self.__request_context.transaction_id,
            created_at=created_at,
            status=status,
            requested_at=self.__request_context.requested_at_isoformat,
            storage_path=storage_path,
            message_type=message_type,
        )

        if self.__environ_context.deployment_id is not None:
            item["deployment_id"] = self.__environ_context.deployment_id

        self.__provider_ddb.put_item(item=item)

        LOGGER.logger.debug("Transaction is now rejected")

        HelperHistoryTransaction(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        ).create(
            history_transaction_new=ModelHistoryTransaction(
                request_id=self.__request_context.request_id,
                requested_at=self.__request_context.requested_at_utc_isoformat,
                transaction_id=self.__request_context.transaction_id,
                status=status,
                message_type=message_type,
                response_code=ht_response_code,
                response_message=ht_response_message,
                currency=currency,
                amount=amount,
                storage_path=storage_path,
            ),
            owner_member_id=self.__request_context.default_owner_id,
        )

        return item

    def pending(self) -> TypeTransaction:
        """
        Pending transaction: insert new row with pending status
        """

        _id: str = str(uuid.uuid4())
        created_at: str = UtilsDatetime().now_isoformat
        status: str = ConstantsTransactionStatus.PENDING.value

        LOGGER.logger.debug("Pending transaction")
        LOGGER.logger.debug(f"\tID {_id}")
        LOGGER.logger.debug(f"\tCREATED AT {created_at}")
        LOGGER.logger.debug(f"\tSTATUS {status}")
        LOGGER.logger.debug(f"\tTRANSACTION ID {self.__request_context.transaction_id}")

        item: TypeTransaction = TypeTransaction(
            id=_id,
            transaction_id=self.__request_context.transaction_id,
            created_at=created_at,
            status=status,
            requested_at=self.__request_context.requested_at_isoformat,
        )

        if self.__environ_context.deployment_id is not None:
            item["deployment_id"] = self.__environ_context.deployment_id

        self.__provider_ddb.put_item(item=item)

        LOGGER.logger.debug("Transaction is now pending")

        return item

    def retrieve(self) -> TypeTransaction:
        """
        Retrieve transaction: insert new row with retrieved status
        :param transaction_id: The id of the transaction
        :type transaction_id: str
        """

        _id: str = str(uuid.uuid4())
        created_at: str = UtilsDatetime().now_isoformat
        status: str = ConstantsTransactionStatus.RETRIEVED.value

        LOGGER.logger.debug("Retrieving transaction")
        LOGGER.logger.debug(f"\tID {_id}")
        LOGGER.logger.debug(f"\tCREATED AT {created_at}")
        LOGGER.logger.debug(f"\tSTATUS {status}")
        LOGGER.logger.debug(f"\tTRANSACTION ID {self.__request_context.transaction_id}")

        item: TypeTransaction = TypeTransaction(
            id=_id,
            transaction_id=self.__request_context.transaction_id,
            created_at=created_at,
            status=status,
            requested_at=self.__request_context.requested_at_isoformat,
        )

        if self.__environ_context.deployment_id is not None:
            item["deployment_id"] = self.__environ_context.deployment_id

        self.__provider_ddb.put_item(item=item)

        LOGGER.logger.debug("Transaction is now retrieved")

        return item

    def notify(
        self,
        storage_path: str,
        message_type: str,
    ) -> TypeTransaction:
        """
        Notify transaction: insert new row with notified status
        :param transaction_id: The id of the transaction
        :type transaction_id: str
        :param storage_path: Path where the XML message is stored
        :type storage_path: str
        :param message_type: Type of the XML message
        :type message_type: str
        """

        _id: str = str(uuid.uuid4())
        created_at: str = UtilsDatetime().now_isoformat
        status: str = ConstantsTransactionStatus.NOTIFIED.value

        LOGGER.logger.debug("Notifying transaction")
        LOGGER.logger.debug(f"\tID {_id}")
        LOGGER.logger.debug(f"\tCREATED AT {created_at}")
        LOGGER.logger.debug(f"\tSTATUS {status}")
        LOGGER.logger.debug(f"\tTRANSACTION ID {self.__request_context.transaction_id}")

        item: TypeTransaction = TypeTransaction(
            id=_id,
            transaction_id=self.__request_context.transaction_id,
            created_at=created_at,
            status=status,
            requested_at=self.__request_context.requested_at_isoformat,
            storage_path=storage_path,
            message_type=message_type,
        )

        if self.__environ_context.deployment_id is not None:
            item["deployment_id"] = self.__environ_context.deployment_id

        self.__provider_ddb.put_item(item=item)

        LOGGER.logger.debug("Transaction is now notified")

        return item

    def release(
        self,
        storage_path: str,
        message_type: str,
        ht_response_code: str,
        ht_response_message: str,
        currency: str,
        amount: str,
    ) -> TypeTransaction:
        """
        :param storage_path: Path where the XML message is stored
        :type storage_path: str
        """

        _id: str = str(uuid.uuid4())
        created_at: str = UtilsDatetime().now_isoformat
        status: str = ConstantsTransactionStatus.RELEASED.value

        LOGGER.logger.debug("Releasing transaction")
        LOGGER.logger.debug(f"\tID {_id}")
        LOGGER.logger.debug(f"\tCREATED AT {created_at}")
        LOGGER.logger.debug(f"\tSTATUS {status}")
        LOGGER.logger.debug(f"\tTRANSACTION ID {self.__request_context.transaction_id}")

        item: TypeTransaction = TypeTransaction(
            id=_id,
            transaction_id=self.__request_context.transaction_id,
            created_at=created_at,
            status=status,
            requested_at=self.__request_context.requested_at_isoformat,
            storage_path=storage_path,
            message_type=message_type,
        )

        if self.__environ_context.deployment_id is not None:
            item["deployment_id"] = self.__environ_context.deployment_id

        self.__provider_ddb.put_item(item=item)

        LOGGER.logger.debug("Transaction is now released")

        HelperHistoryTransaction(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        ).create(
            history_transaction_new=ModelHistoryTransaction(
                request_id=self.__request_context.request_id,
                requested_at=self.__request_context.requested_at_utc_isoformat,
                transaction_id=self.__request_context.transaction_id,
                status=status,
                message_type=message_type,
                response_code=ht_response_code,
                response_message=ht_response_message,
                currency=currency,
                amount=amount,
                storage_path=storage_path,
            ),
            owner_member_id=self.__request_context.default_owner_id,
        )

        return item

    def fail(self) -> TypeTransaction:
        """
        Fail transaction: insert new row with failed status
        """

        _id: str = str(uuid.uuid4())
        created_at: str = UtilsDatetime().now_isoformat
        status: str = ConstantsTransactionStatus.FAILED.value

        LOGGER.logger.info("Failing transaction")
        LOGGER.logger.info(f"\tID {_id}")
        LOGGER.logger.info(f"\tCREATED AT {created_at}")
        LOGGER.logger.info(f"\tSTATUS {status}")
        LOGGER.logger.info(f"\tTRANSACTION ID {self.__request_context.transaction_id}")

        item: TypeTransaction = TypeTransaction(
            id=_id,
            transaction_id=self.__request_context.transaction_id,
            created_at=created_at,
            status=status,
            requested_at=self.__request_context.requested_at_isoformat,
        )

        if self.__environ_context.deployment_id is not None:
            item["deployment_id"] = self.__environ_context.deployment_id

        self.__provider_ddb.put_item(item=item)

        LOGGER.logger.info("Transaction is now failed")

        return item

    def retrieved(self) -> None:
        """
        Update retrieved=true attribute associated
        with either RELEASED, REJECTED, CANCELED or NOTIFIED status
        :param retrieved_at: Time of the retrieve request
        :type retrieved_at: str
        """

        LOGGER.logger.debug(
            "Querying the table."
            + " Retrieving count RELEASED, REJECTED, CANCELED or NOTIFIED"
            + f" status for transaction with id {self.__request_context.transaction_id}"
        )

        result: QueryOutputTypeDef = self.__provider_ddb.ddb_table.scan(
            FilterExpression=Attr("status").is_in(
                [
                    ConstantsTransactionStatus.RELEASED.value,
                    ConstantsTransactionStatus.REJECTED.value,
                    ConstantsTransactionStatus.CANCELED.value,
                    ConstantsTransactionStatus.NOTIFIED.value,
                ]
            )
            & Attr("transaction_id").eq(self.__request_context.transaction_id),
        )

        LOGGER.logger.debug(
            f"Finished running the query. Total count is {result.get('Count')}"
        )

        if result.get("Count") == 0:
            return

        for item in result.get("Items"):
            _item: TypeTransaction = TypeTransaction(item)
            _item.retrieved_at = self.__request_context.requested_at_isoformat

            LOGGER.logger.debug("Updating transaction... Adding retrieved attribute")
            LOGGER.logger.debug(f"\tID {_item.id}")
            LOGGER.logger.debug(f"\tCREATED AT {_item.created_at}")
            LOGGER.logger.debug(f"\tSTATUS {_item.status}")
            LOGGER.logger.debug(f"\tTRANSACTION ID {_item.transaction_id}")
            LOGGER.logger.debug(f"\tRETRIEVED AT {_item.retrieved_at}")

            self.__provider_ddb.put_item(item=_item)

            LOGGER.logger.debug("Transaction now has retrieved_at attribute")

    def transaction_status_all_count(self) -> int:
        """
        Retrieve the count of all states for a transaction
        """

        LOGGER.logger.debug(
            "Querying the table. "
            + f"Retrieving count of all rows for transaction ID {self.__request_context.transaction_id}"
        )

        result: QueryOutputTypeDef = self.__provider_ddb.ddb_table.query(
            IndexName="gsi-transactionid",
            KeyConditionExpression=Key("transaction_id").eq(
                self.__request_context.transaction_id
            ),
            Select="COUNT",
        )
        count: int = result.get("Count")

        LOGGER.logger.debug(f"Finished running the query. Total count is {count}")

        return count

    def is_transaction_pending(self) -> bool:
        """
        Check if the specified transaction_id has the PENDING status
        """

        LOGGER.logger.debug(
            "Querying the table. "
            + f"Counting all rows with PENDING status for transaction ID {self.__request_context.transaction_id}"
        )

        result: QueryOutputTypeDef = self.__provider_ddb.ddb_table.query(
            IndexName="gsi-status",
            KeyConditionExpression=Key("status").eq(
                ConstantsTransactionStatus.PENDING.value
            )
            & Key("transaction_id").eq(self.__request_context.transaction_id),
        )

        count: int = result.get("Count")

        LOGGER.logger.debug(f"Finished running the query. Total count is {count}")

        return count > 0

    def is_transaction_initiated(self) -> bool:
        """
        Check if the specified transaction_id has the INITIATED status
        :param transaction_id: The id of the transaction
        :type transaction_id: str
        """

        LOGGER.logger.debug(
            f"Checking if transaction with id {self.__request_context.transaction_id} is valid and initiated"
        )

        LOGGER.logger.debug("Retrieving transaction TTL from environment")

        ttl: int = self.__environ_context.msa_uuid_ttl

        LOGGER.logger.debug(f"Transaction TTL is {ttl} seconds")

        # Count of rows with specified transaction id
        result_status: int = self.transaction_status_all_count()

        result_transaction: QueryOutputTypeDef = self.__provider_ddb.ddb_table.query(
            IndexName="gsi-status",
            KeyConditionExpression=Key("status").eq(
                ConstantsTransactionStatus.INITIATED.value
            )
            & Key("transaction_id").eq(self.__request_context.transaction_id),
        )

        if result_status != 1 or result_transaction.get("Count") != 1:
            # No rows matching the specified transaction id were found
            # Too many rows matching the specified transaction id were found; it was already processed
            LOGGER.logger.error(
                "Transaction was already processed or was not initiated"
            )
            return False

        item: TypeTransaction = TypeTransaction(result_transaction.get("Items")[0])
        created_at: str = item.created_at
        created_at_d: datetime.datetime = None

        try:
            created_at_d = datetime.datetime.fromisoformat(created_at)
        except ValueError as exc:
            raise ExceptionUnexpectedError(
                request_context=self.__request_context,
                message=str(exc),
            ) from exc

        # TODO use datetime utils
        diff: int = round(
            (datetime.datetime.now().astimezone() - created_at_d).total_seconds()
        )

        LOGGER.logger.debug(
            f"Transaction was created aprox. {diff} seconds ago. Checking if it is above the allowed TTL"
        )

        lte_ttl: bool = diff <= ttl

        LOGGER.logger.debug(f"Transaction is expired? {lte_ttl}")

        return lte_ttl

    def exists(self) -> bool:
        """
        Check if the specified transaction_id exists
        """

        LOGGER.logger.debug(
            "Querying the table. "
            + f"Retrieving count of all rows for transaction with id {self.__request_context.transaction_id}"
        )

        result: QueryOutputTypeDef = self.__provider_ddb.ddb_table.query(
            IndexName="gsi-transactionid",
            KeyConditionExpression=Key("transaction_id").eq(
                self.__request_context.transaction_id
            ),
            Select="COUNT",
        )
        count: int = result.get("Count")

        LOGGER.logger.debug(f"Finished running the query. Total count is {count}")

        return count > 0
