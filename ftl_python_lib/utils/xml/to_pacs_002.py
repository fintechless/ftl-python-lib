"""
PACS-008 & PACS-002 messages conversions
"""

import copy
from typing import Dict
from typing import Union


def pacs_008_to_pacs_002(
    src: Union[Dict[str, str], dict]
) -> Union[Dict[str, str], dict]:
    if isinstance(src, dict) is False:
        raise ValueError(
            f"Received invalid type '{type(src).__name__}'. Must be 'dict'"
        )
    res = copy.deepcopy(src)
    res["Document"]["@xmlns"] = "urn:iso:std:iso:20022:tech:xsd:pacs.002.001.12"

    return res
