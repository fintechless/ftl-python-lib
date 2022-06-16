"""
Rabbitmq
To be inherited by upper class exception
"""

import ssl

import pika

from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.decorators.exponential_backoff import DecoratorExponentialBackoff


class Rabbitmq:
    """
    Rabbitmq class
    :param __rabbitmq_username: Rabbitmq username
    :type __rabbitmq_username: str
    :param __rabbitmq_password: Rabbitmq password
    :type __rabbitmq_password: str
    :param __rabbitmq_endpoint: Rabbitmq amqps
    :type __rabbitmq_endpoint: str
    :param __rabbitmq_port: Rabbitmq port
    :type __rabbitmq_port: str
    """

    def __init__(
        self,
        rabbitmq_username: str,
        rabbitmq_password: str,
        rabbitmq_endpoint: str,
        rabbitmq_port: str,
    ) -> None:
        """
        Constructor
        :param rabbitmq_username: Rabbitmq username
        :type rabbitmq_username: str
        :param rabbitmq_password: Rabbitmq password
        :type rabbitmq_password: str
        :param rabbitmq_endpoint: Rabbitmq amqps
        :type rabbitmq_endpoint: str
        :param rabbitmq_port: Rabbitmq port
        :type rabbitmq_port: str
        """

        LOGGER.logger.debug(f"Request to: {rabbitmq_endpoint+':'+rabbitmq_port}")

        self.__rabbitmq_username = rabbitmq_username
        self.__rabbitmq_password = rabbitmq_password
        self.__rabbitmq_endpoint = rabbitmq_endpoint
        self.__rabbitmq_port = rabbitmq_port

    @DecoratorExponentialBackoff.retry(Exception)
    def connection(self):
        credentials = pika.PlainCredentials(
            self.__rabbitmq_username, self.__rabbitmq_password
        )
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        parameters = pika.ConnectionParameters(
            self.__rabbitmq_endpoint,
            credentials=credentials,
            port=self.__rabbitmq_port,
            ssl_options=pika.SSLOptions(context),
            virtual_host="/",
        )
        return pika.BlockingConnection(parameters)

    @DecoratorExponentialBackoff.retry(Exception)
    def get_properties(self, app_id: str, content_type: str, transaction_queue: str):
        hdrs = {"X-MESSAGE-TYPE": transaction_queue}
        return pika.BasicProperties(
            app_id=app_id, content_type=content_type, headers=hdrs
        )

    @DecoratorExponentialBackoff.retry(Exception)
    def push_message(self, main_channel, xml_data, properties, exchange, routing_key):
        main_channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=xml_data,
            properties=properties,
        )
