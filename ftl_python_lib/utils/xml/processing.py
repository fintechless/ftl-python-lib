"""
Utility for XML processing
"""

from typing import Dict
from typing import Union

import xmltodict

from ftl_python_lib.utils.to_str import bytes_to_str


def unparse(src: Union[Dict[str, str], dict]) -> str:
    """
    Convert Python dict to XML string
    """
    return xmltodict.unparse(input_dict=src)


def parse(src: Union[str, bytes]) -> Union[Dict[str, str], dict]:
    """
    Convert Python dict to XML string
    """

    if isinstance(src, bytes):
        return xmltodict.parse(xml_input=bytes_to_str(src=src))

    return xmltodict.parse(xml_input=src)
