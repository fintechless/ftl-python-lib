"""
"""

from enum import Enum

from ftl_python_lib.constants.kubernetes import ConstantsKubernetesServiceNames
from ftl_python_lib.constants.kubernetes import service_url


class ConstantsMicroservicesNames(Enum):
    MSA_MESSAGE_IN = "ftl-msa-msg-in"
    MSA_MESSAGE_OUT = "ftl-msa-msg-out"
    MSA_RMQ_OUT = "ftl-msa-rmq-out"
    MSA_RMQ_IN = "ftl-msa-rmq-in"
    MSA_MSG_PACS_008 = "ftl-msa-msg-pacs-008"

    API_MAPPING = "ftl-api-mapping"


class ConstantsMicroservicesHttpPort(Enum):
    PORT = 5000


class ConstantsMictoservicesHttp(Enum):
    MSA_MESSAGE_IN = service_url(
        service_name=ConstantsKubernetesServiceNames.MSA_MESSAGE_IN.value,
        url_prefix="msa/in",
    )
    MSA_MESSAGE_OUT = service_url(
        service_name=ConstantsKubernetesServiceNames.MSA_MESSAGE_OUT.value,
        url_prefix="msa/out",
    )
    MSA_RMQ_OUT = service_url(
        service_name=ConstantsKubernetesServiceNames.MSA_RMQ_OUT.value,
        url_prefix="msa/rmq/out",
    )
    MSA_RMQ_IN = service_url(
        service_name=ConstantsKubernetesServiceNames.MSA_RMQ_IN.value,
        url_prefix="msa/rmq/in",
    )
    MSA_MSG_PACS_008 = service_url(
        service_name=ConstantsKubernetesServiceNames.MSA_MSG_PACS_008.value,
        url_prefix="msa/pacs-008",
    )

    API_MAPPING = service_url(
        service_name=ConstantsKubernetesServiceNames.API_MAPPING.value,
        url_prefix="msa/mapping",
    )
