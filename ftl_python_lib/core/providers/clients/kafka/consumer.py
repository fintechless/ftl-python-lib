"""
Provider for Kafka Consumer
"""

from typing import List
from typing import Optional

from confluent_kafka import Consumer
from confluent_kafka import Message

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.exceptions.server_unexpected_error_exception import ExceptionUnexpectedError
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.utils.to_str import bytes_to_str


# pylint: disable=R0903
# too-few-public-methods
class ProviderKafkaConsumer:
    """
    Provider for Kafka Consumer
    :param __bootstrap_servers: Kafka bootstrap servers for connection
    :type __bootstrap_servers: str
    :param __request_context: Context about the request
    :type __request_context: RequestContext
    :param __subscribed: Is consumer subscribed?
    :param __subscribed: bool
    :param __consumer: Kafka consumer
    :type __consumer: Optional[Consumer]
    """

    def __init__(
        self,
        request_context: RequestContext,
        environ_context: EnvironmentContext,
        init_consumer: Optional[bool] = True,
    ) -> None:
        """
        Constructor
        :param request_context: Context about the request
        :type request_context: RequestContext
        :param init_consumer: Initiate consumer during class construct
        :type init_consumer: Optional[bool]
        """

        LOGGER.logger.debug("Creating new Kafka consumer")
        LOGGER.logger.debug(f"FTL Request ID: {request_context.request_id}")

        self.__request_context = request_context
        self.__environ_context = environ_context
        self.__bootstrap_servers = self.__environ_context.kafka_broker_endpoints

        self.__subscribed = False

        if init_consumer is True:
            LOGGER.logger.debug("Initializing Kafka consumer. Connecting to brokers")

            self.__consumer = Consumer(
                {
                    "bootstrap.servers": self.__bootstrap_servers,
                    "group.id": __package__,
                    "enable.auto.commit": False,
                    "auto.offset.reset": "earliest",
                }
            )

            LOGGER.logger.debug("Initializing Kafka consumer. Connected to brokers")
        else:
            LOGGER.logger.debug("Kafka consumer will not be initialized")

            self.__consumer = None

    def init_consumer(self) -> None:
        """
        Create Kafka consumer and create a connection
        """

        LOGGER.logger.debug("Initializing Kafka consumer. Connecting to brokers")

        self.__consumer = Consumer(
            {
                "bootstrap.servers": self.__bootstrap_servers,
                "group.id": __package__,
                "enable.auto.commit": False,
                "auto.offset.reset": "earliest",
            }
        )

        LOGGER.logger.debug("Initializing Kafka consumer. Connected to brokers")

    def subscribe(self, topics: List[str]) -> None:
        """
        Set subscription to supplied list of topics
        :param topics: List of topic to subscribe to
        :type topics: List[str]
        """

        if self.__consumer is not None:
            LOGGER.logger.debug(
                f"Kafka consumer is initialized. Subscribing to topics: {topics}"
            )

            self.__consumer.subscribe(topics)
            self.__subscribed = True

            LOGGER.logger.debug(f"Subscribed to topics: {topics}")

    def poll(self, timeout: Optional[float] = 1.0) -> Optional[Message]:
        """
        Consume a single message
        :param timeout: Maximum time to block waiting for message
        :type timeout: Optional[float]
        """

        if self.__subscribed is True and self.__consumer is not None:
            LOGGER.logger.debug(
                "Kafka consumer is intialized and subscribed. Polling for new message"
            )

            return self.__consumer.poll(timeout=timeout)
        raise ExceptionUnexpectedError(
            request_context=self.__request_context,
            message="Kafka consumer was not subscribed",
        )

    def commit(self, message: Optional[None]) -> None:
        """
        Commit a message
        """

        if message is None:
            LOGGER.logger.warning("Empty message will not be commited")

            return

        if self.__subscribed is True and self.__consumer is not None:
            key: str = bytes_to_str(message.key())

            LOGGER.logger.debug(
                f"Kafka consumer is intialized and subscribed. Commiting message with key: {key}"
            )

            self.__consumer.commit(message=message)

    def close(self) -> None:
        """
        Close down and terminate the Kafka Consumer
        """

        if self.__subscribed is True and self.__consumer is not None:
            LOGGER.logger.debug(
                "Kafka consumer is intialized and subscribed. Closing the consumer"
            )

            self.__consumer.close()
