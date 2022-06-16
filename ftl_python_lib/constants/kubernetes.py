"""
"""

from enum import Enum


def service_url(service_name: str, url_prefix: str) -> str:
    """
    Generate Kubernetes service URL
    """

    namespace: str = ConstantsKubernetes.NAMESPACE.value
    service_port: int = ConstantsKubernetes.SERVICE_PORT.value

    return f"{service_name}.{namespace}.svc.cluster.local:{service_port}/{url_prefix}"


class ConstantsKubernetes(Enum):
    NAMESPACE = "fintechless"
    SERVICE_PORT = 5000


class ConstantsKubernetesServiceNames(Enum):
    MSA_MESSAGE_IN = "msa-msg-in-svc"
    MSA_MESSAGE_OUT = "msa-msg-out-svc"
    MSA_RMQ_OUT = "msa-rmq-out-svc"
    MSA_MSG_PACS_008 = "msa-msg-pacs-008-svc"

    API_MAPPING = "msa-msg-mapping-svc"
