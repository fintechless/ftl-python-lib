"""
Context for the FTL environment
Manage FTL environment variables
"""

import json
import os
from typing import Dict
from typing import Optional

from ftl_python_lib.core.providers.aws.secretsmanager_environ import ProviderSecretsManagerEnviron


def push_environ_to_os():
    current_environ: EnvironmentContext = EnvironmentContext()
    provider_secretsmanager: ProviderSecretsManagerEnviron = (
        ProviderSecretsManagerEnviron(environ_context=current_environ)
    )
    secrets: Dict[str, str] = provider_secretsmanager.get_value()

    for key, value in secrets.items():
        if isinstance(value, int):
            os.environ[key] = str(value)
        elif isinstance(value, dict):
            os.environ[key] = json.dumps(value)
        else:
            os.environ[key] = value


class EnvironmentContext:
    """
    FTL Context about the current environment
    """

    def __get_value(self, key: str, silent: bool = False) -> str:
        """
        Get environment variable value using its key
        :param key: environment variable key
        :type key: str
        :param silent: Handle the exception silently or not
        :type silent: bool
        """

        value: Optional[str] = os.environ.get(key)

        if value is None and silent is False:
            raise ValueError(f"Environment variable {key} is missing")
        return value

    @property
    def environment(self) -> str:
        """
        Get FTL_ENVIRONMENT env variable value
        """

        return self.__get_value(key="FTL_ENVIRONMENT")

    @property
    def environment_context_secret_name(self) -> str:
        """
        Get FTL_ENVIRON_CONTEXT_SECRET env variable value
        """

        return self.__get_value(key="FTL_ENVIRON_CONTEXT_SECRET")

    @property
    def deployment_id(self) -> str:
        """
        Get FTL_DEPLOYMENT_ID env variable value
        """

        return self.__get_value(key="FTL_DEPLOYMENT_ID")

    @property
    def api_domain(self) -> str:
        """
        Get FTL_API_DOMAIN env variable value
        """

        return self.__get_value(key="FTL_API_DOMAIN")

    @property
    def cloud_provider(self) -> str:
        """
        Get FTL_CLOUD_PROVIDER env variable value
        """

        return self.__get_value(key="FTL_CLOUD_PROVIDER")

    @property
    def cloud_provider_api_endpoint_url(self) -> str:
        """
        Get FTL_CLOUD_PROVIDER_API_ENDPOINT_URL env variable value
        """

        return self.__get_value(key="FTL_CLOUD_PROVIDER_API_ENDPOINT_URL", silent=True)

    @property
    def cloud_region_primary(self) -> str:
        """
        Get FTL_CLOUD_REGION_PRIMARY env variable value
        """

        return self.__get_value(key="FTL_CLOUD_REGION_PRIMARY")

    @property
    def cloud_region_secondary(self) -> str:
        """
        Get FTL_CLOUD_REGION_SECONDARY env variable value
        """

        return self.__get_value(key="FTL_CLOUD_REGION_SECONDARY")

    @property
    def msa_uuid_ttl(self) -> int:
        """
        Get FTL_MSA_UUID_TTL env variable value
        """

        return (
            int(self.__get_value(key="FTL_MSA_UUID_TTL"))
            if self.__get_value(key="FTL_MSA_UUID_TTL").isdigit()
            else 5
        )

    @property
    def msa_latest_limit(self) -> int:
        """
        Get FTL_MSA_LATEST_LIMIT env variable value
        """

        return (
            int(self.__get_value(key="FTL_MSA_LATEST_LIMIT"))
            if self.__get_value(key="FTL_MSA_LATEST_LIMIT").isdigit()
            else 5
        )

    @property
    def runtime_bucket(self) -> str:
        """
        Get FTL_RUNTIME_BUCKET env variable value
        """

        return self.__get_value(key="FTL_RUNTIME_BUCKET")

    @property
    def deploy_bucket(self) -> str:
        """
        Get FTL_DEPLOY_BUCKET env variable value
        """

        return self.__get_value(key="FTL_DEPLOY_BUCKET")

    @property
    def runtime_secretsmanager(self) -> str:
        """
        Get FTL_RUNTIME_SECRETSMANAGER env variable value
        """

        return self.__get_value(key="FTL_RUNTIME_SECRETSMANAGER")

    @property
    def kafka_broker_endpoints(self) -> str:
        """
        Get KAFKA_BROKER env variable value
        """

        return self.__get_value(key="KAFKA_BROKER")

    @property
    def kafka_message_inbox_target(self) -> str:
        """
        Get KAFKA_MESSAGE_INBOX_TARGET env variable value
        """

        return self.__get_value(key="KAFKA_MESSAGE_INBOX_TARGET")

    @property
    def kafka_message_outbox_target(self) -> str:
        """
        Get KAFKA_MESSAGE_OUTBOX_TARGET env variable value
        """

        return self.__get_value(key="KAFKA_MESSAGE_OUTBOX_TARGET")

    @property
    def msa_msg_out(self) -> str:
        """
        Get FTL_MSA_MSG_OUT env variable value
        """

        return self.__get_value(key="FTL_MSA_MSG_OUT")

    @property
    def msa_msg_in(self) -> str:
        """
        Get FTL_MSA_MSG_IN env variable value
        """

        return self.__get_value(key="FTL_MSA_MSG_IN")

    @property
    def aws_cognito_user_pool_id(self) -> str:
        """
        Get AWS_COGNITO_USER_POOL_ID env variable value
        """

        return self.__get_value(key="AWS_COGNITO_USER_POOL_ID")

    @property
    def aws_cognito_client_secret(self) -> str:
        """
        Get AWS_COGNITO_CLIENT_SECRET env variable value
        """

        return self.__get_value(key="AWS_COGNITO_CLIENT_SECRET")

    @property
    def aws_cognito_user_username(self) -> str:
        """
        Get AWS_COGNITO_USER_USERNAME env variable value
        """

        return self.__get_value(key="AWS_COGNITO_USER_USERNAME")

    @property
    def aws_cognito_user_password(self) -> str:
        """
        Get AWS_COGNITO_USER_PASSWORD env variable value
        """

        return self.__get_value(key="AWS_COGNITO_USER_PASSWORD")

    @property
    def ftl_fqdn(self) -> str:
        """
        Get FTL_FQDN env variable value
        """

        return self.__get_value(key="FTL_FQDN")

    @property
    def ftl_region(self) -> str:
        """
        Get FTL_REGION env variable value
        """

        return self.__get_value(key="FTL_REGION")

    @property
    def ftl_msa_in(self) -> str:
        """
        Get FTL_MSA_IN env variable value
        """

        return self.__get_value(key="FTL_MSA_IN")

    @property
    def ftl_msa_uuid(self) -> str:
        """
        Get FTL_MSA_UUID env variable value
        """

        return self.__get_value(key="FTL_MSA_UUID")

    @property
    def ftl_msa_target(self) -> str:
        """
        Get FTL_MSA_TARGET env variable value
        """

        return self.__get_value(key="FTL_MSA_TARGET")

    @property
    def ftl_queue_target(self) -> str:
        """
        Get FTL_QUEUE_TARGET env variable value
        """

        return self.__get_value(key="FTL_QUEUE_TARGET")

    @property
    def ftl_entity_source(self) -> str:
        """
        Get FTL_ENTITY_SOURCE env variable value
        """

        return self.__get_value(key="FTL_ENTITY_SOURCE")

    @property
    def ftl_entity_target(self) -> str:
        """
        Get FTL_ENTITY_TARGET env variable value
        """

        return self.__get_value(key="FTL_ENTITY_TARGET")

    @property
    def rabbitmq_endpoint(self) -> str:
        """
        Get RABBITMQ_ENDPOINT env variable value
        """

        return self.__get_value(key="RABBITMQ_ENDPOINT")

    @property
    def rabbitmq_password(self) -> str:
        """
        Get RABBITMQ_PASSWORD env variable value
        """

        return self.__get_value(key="RABBITMQ_PASSWORD")

    @property
    def rabbitmq_username(self) -> str:
        """
        Get RABBITMQ_USERNAME env variable value
        """

        return self.__get_value(key="RABBITMQ_USERNAME")

    @property
    def rabbitmq_port(self) -> str:
        """
        Get RABBITMQ_PORT env variable value
        """

        return self.__get_value(key="RABBITMQ_PORT")

    @property
    def rabbitmq_endpoint_amqps(self) -> str:
        """
        Get RABBITMQ_ENDPOINT_AMQPS env variable value
        """

        return self.__get_value(key="RABBITMQ_ENDPOINT_AMQPS")

    @property
    def rabbitmq_endpoint_public(self) -> str:
        """
        Get RABBITMQ_ENDPOINT_PUBLIC env variable value
        """

        return self.__get_value(key="RABBITMQ_ENDPOINT_PUBLIC")

    @property
    def rabbitmq_exchange(self) -> str:
        """
        Get RABBITMQ_EXCHANGE env variable value
        """

        return self.__get_value(key="RABBITMQ_EXCHANGE")

    @property
    def rabbitmq_queue(self) -> str:
        """
        Get RABBITMQ_QUEUE env variable value
        """

        return self.__get_value(key="RABBITMQ_QUEUE")

    @property
    def rabbitmq_routing_key(self) -> str:
        """
        Get RABBITMQ_ROUTING_KEY env variable value
        """

        return self.__get_value(key="RABBITMQ_ROUTING_KEY")

    @property
    def src_parallel_count(self) -> str:
        """
        Get SRC_PARALLEL_COUNT env variable value
        """

        return int(self.__get_value(key="SRC_PARALLEL_COUNT"))

    @property
    def ftl_db_engine(self) -> str:
        """
        Get FTL_DB_ENGINE env variable value
        """

        return int(self.__get_value(key="FTL_DB_ENGINE"))

    @property
    def ftl_db_username(self) -> str:
        """
        Get FTL_DB_USERNAME env variable value
        """

        return self.__get_value(key="FTL_DB_USERNAME")

    @property
    def ftl_db_password(self) -> str:
        """
        Get FTL_DB_PASSWORD env variable value
        """

        return self.__get_value(key="FTL_DB_PASSWORD")

    @property
    def ftl_db_host(self) -> str:
        """
        Get FTL_DB_HOST env variable value
        """

        return self.__get_value(key="FTL_DB_HOST")

    @property
    def ftl_db_database(self) -> str:
        """
        Get FTL_DB_DATABASE env variable value
        """

        return self.__get_value(key="FTL_DB_DATABASE")

    @property
    def ftl_db_port(self) -> str:
        """
        Get FTL_DB_PORT env variable value
        """

        return self.__get_value(key="FTL_DB_PORT")

    @property
    def message_definitions_host(self) -> str:
        """
        Get MESSAGE_DEFINITIONS_HOST env variable value
        """

        return self.__get_value(key="MESSAGE_DEFINITIONS_HOST")

    @property
    def owner_first_name(self) -> str:
        """
        Get FTL_OWNER_FIRST_NAME env variable value
        """

        return self.__get_value(key="FTL_OWNER_FIRST_NAME")

    @property
    def owner_last_name(self) -> str:
        """
        Get FTL_OWNER_LAST_NAME env variable value
        """

        return self.__get_value(key="FTL_OWNER_LAST_NAME")

    @property
    def owner_email(self) -> str:
        """
        Get FTL_OWNER_EMAIL env variable value
        """

        return self.__get_value(key="FTL_OWNER_EMAIL")
