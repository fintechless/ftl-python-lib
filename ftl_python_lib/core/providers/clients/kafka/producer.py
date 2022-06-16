"""
Provider for Kafka Producer
"""

from typing import Optional

from confluent_kafka import Producer

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.exceptions.server_unexpected_error_exception import ExceptionUnexpectedError
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.utils.to_str import bytes_to_str


class ProviderKafkaProducer:
    """
    Provider for Kafka Producer
    :param __bootstrap_servers: Kafka bootstrap servers for connection
    :type __bootstrap_servers: str
    :param __request_context: Context about the request
    :type __request_context: RequestContext
    :param __producer: Kafka producer
    :type __producer: Optional[Producer]
    """

    def __init__(
        self,
        request_context: RequestContext,
        environ_context: EnvironmentContext,
        init_producer: Optional[bool] = True,
    ) -> None:
        """
        Constructor
        :param bootstrap_servers: Kafka bootstrap servers for connection
        :type bootstrap_servers: str
        :param request_context: Context about the request
        :type request_context: RequestContext
        :param init_producer: Initiate producer during class construct
        :type init_producer: Optional[bool]
        """

        LOGGER.logger.debug("Creating new Kafka producer")
        LOGGER.logger.debug(f"FTL Request ID: {request_context.request_id}")

        self.__request_context = request_context
        self.__environ_context = environ_context
        self.__bootstrap_servers = self.__environ_context.kafka_broker_endpoints

        if init_producer is True:
            LOGGER.logger.debug("Initializing Kafka producer. Connecting to brokers")

            self.__producer = Producer(
                {
                    "bootstrap.servers": self.__bootstrap_servers,
                    "client.id": __package__,
                }
            )

            LOGGER.logger.debug("Initializing Kafka producer. Connected to brokers")
        else:
            LOGGER.logger.debug("Kafka producer will not be initialized")

            self.__producer = None

    def init_producer(self) -> None:
        """
        Create Kafka producer and create a connection
        """

        LOGGER.logger.debug("Initializing Kafka producer. Connecting to brokers")

        self.__producer = Producer(
            {
                "bootstrap.servers": self.__bootstrap_servers,
                "client.id": __package__,
            }
        )

        LOGGER.logger.debug("Initializing Kafka producer. Connected to brokers")

    def produce_message_in_sync(self, key: str, value: str) -> None:
        """
        Produce a Kafka message - incoming topic
        :param key: Message key
        :type key: str
        :param value: Message value
        :type value: str
        """

        if self.__producer is not None:
            LOGGER.logger.debug(
                f"Kafka producer is initialized. Producing message with key: {key}"
            )

            self.__producer.produce(
                topic=self.__environ_context.kafka_message_inbox_target,
                key=key,
                value=value,
                callback=self.delivery_callback,
            )
            self.__producer.flush()

    def produce_message_out_sync(self, key: str, value: str) -> None:
        """
        Produce a Kafka message - outgoing topic
        :param key: Message key
        :type key: str
        :param value: Message value
        :type value: str
        """

        if self.__producer is not None:
            LOGGER.logger.debug(
                f"Kafka producer is initialized. Producing message with key: {key}"
            )

            self.__producer.produce(
                topic=self.__environ_context.kafka_message_outbox_target,
                key=key,
                value=value,
                callback=self.delivery_callback,
            )
            self.__producer.flush()

    def delivery_callback(self, error: str, message: str) -> None:
        """
        Kafka producer callback
        Will be called after each successful/unsuccessful messsage delivery
        """

        if error is not None:
            LOGGER.logger.error(f"Could not produce message in Kafka topic: {error}")

            raise ExceptionUnexpectedError(
                message=error, request_context=self.__request_context
            )

        key: str = bytes_to_str(src=message.key())
        LOGGER.logger.debug(
            f"Produced message with key {key} to Kafka topic {message.topic()}[{message.partition()}]"
        )
