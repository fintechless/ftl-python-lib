from typing import Literal
from typing import Union

from ftl_python_lib.constants.microservices import ConstantsMicroservicesNames
from ftl_python_lib.core.microservices.api.mapping import MicroserviceApiMapping
from ftl_python_lib.core.microservices.msa.msg_out import MicroserviceMsaMsgOut
from ftl_python_lib.core.microservices.msa.msg_pacs_008 import MicroserviceMsaMsgPacs008
from ftl_python_lib.core.microservices.msa.rmq_in import MicroserviceMsaRmqIn
from ftl_python_lib.core.microservices.msa.rmq_out import MicroserviceMsaRmqOut


def which_microservice_am_i(
    name: Union[
        str,
        Literal[ConstantsMicroservicesNames.API_MAPPING],
        Literal[ConstantsMicroservicesNames.MSA_MESSAGE_IN],
        Literal[ConstantsMicroservicesNames.MSA_MESSAGE_OUT],
        Literal[ConstantsMicroservicesNames.MSA_MSG_PACS_008],
        Literal[ConstantsMicroservicesNames.MSA_RMQ_OUT],
        Literal[ConstantsMicroservicesNames.MSA_RMQ_IN],
    ]
):
    if name in (
        ConstantsMicroservicesNames.API_MAPPING.value,
        ConstantsMicroservicesNames.API_MAPPING,
    ):
        return MicroserviceApiMapping
    # if name == ConstantsMicroservicesNames.MSA_MESSAGE_IN.value:
    #   pass
    if name in (
        ConstantsMicroservicesNames.MSA_MESSAGE_OUT.value,
        ConstantsMicroservicesNames.MSA_MESSAGE_OUT,
    ):
        return MicroserviceMsaMsgOut
    if name in (
        ConstantsMicroservicesNames.MSA_MSG_PACS_008.value,
        ConstantsMicroservicesNames.MSA_MSG_PACS_008,
    ):
        return MicroserviceMsaMsgPacs008
    if name in (
        ConstantsMicroservicesNames.MSA_RMQ_OUT.value,
        ConstantsMicroservicesNames.MSA_RMQ_OUT,
    ):
        return MicroserviceMsaRmqOut
    if name in (
        ConstantsMicroservicesNames.MSA_RMQ_IN.value,
        ConstantsMicroservicesNames.MSA_RMQ_IN,
    ):
        return MicroserviceMsaRmqIn

    raise ValueError(f"Could not find microservice with name '{name}'")
