"""
Constants for Mapping
"""

from enum import Enum


class ConstantsMappingInFailedOut(Enum):
    PACS_002 = "pacs.008"


class ConstantsMappingSourceType(Enum):
    """
    Mapping dictionary class - inherits the Enum class
    """

    SOURCE_MESSAGE_IN = "ftl-msa-msg-in"
    SOURCE_TYPE_MESSAGE_IN = "message_in"

    SOURCE_MESSAGE_PACS_008 = "ftl-msa-msg-pacs-008"

    SOURCE_MESSAGE_OUT = "ftl-msa-msg-out"
    SOURCE_TYPE_MESSAGE_OUT = "message_out"

    SOURCE_KAFKA_IN = "ftl-msa-kafka-in"
    SOURCE_TYPE_KAFKA_IN = "kafka_in"

    SOURCE_KAFKA_OUT = "ftl-msa-kafka-out"
    SOURCE_TYPE_KAFKA_OUT = "kafka_out"

    SOURCE_RMQ_IN = "ftl-msa-rmq-in"
    SOURCE_TYPE_RMQ_IN = "rmq_in"

    SOURCE_RMQ_OUT = "ftl-msa-rmq-out"
    SOURCE_TYPE_RMQ_OUT = "rmq_out"
