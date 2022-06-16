"""
Utility for XML validation
"""

import os
import tempfile
from types import TracebackType
from typing import Optional
from typing import Type
from typing import Union
from xml.etree import ElementTree

from lxml import etree

from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.utils.to_str import bytes_to_str


class UtilsXmlValidation:
    """
    Validate XML using XSD schema
    """

    # XML path on local disk
    __xmlp: str = None
    # XSD path on local disk
    __xsdp: str = None
    # etree Schema
    __xmlschema: etree.XMLSchema = None

    def __init__(self, xsd: Union[bytes, str], xml: Union[bytes, str]) -> None:
        """
        Constructor
        :param xsd: XSD schema
        :type xsd: Union[bytes, str]
        :param xml: XML which needs to be validated
        :type xml: Union[bytes, str]
        """

        LOGGER.logger.debug("Constructing new XML Validation")

        self.__xsd = xsd
        self.__xml = xml

    def __enter__(self):
        """
        Entry point of the context
        """

        # Saving XSD to file
        LOGGER.logger.debug("Writing XSD to file")

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_xsd:
            if isinstance(self.__xsd, bytes):
                LOGGER.logger.debug("XSD is in bytes format. Converting")

                tmp_xsd.write(bytes_to_str(src=self.__xsd))
            else:
                LOGGER.logger.debug("XSD is in string format. Skip conversion")

                tmp_xsd.write(self.__xsd)

            self.__xsdp = tmp_xsd.name

            LOGGER.logger.debug(f"XSD written to file {self.__xsdp}")

        _xsd: ElementTree = etree.parse(source=self.__xsdp)
        self.__xmlschema = etree.XMLSchema(etree=_xsd)

        # Saving XML to file
        LOGGER.logger.debug("Writing XML to file")

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_xml:
            if isinstance(self.__xml, bytes):
                LOGGER.logger.debug("XML is in bytes format. Converting")

                tmp_xml.write(bytes_to_str(src=self.__xml))
            else:
                LOGGER.logger.debug("XML is in string format. Skip conversion")

                tmp_xml.write(self.__xml)

            self.__xmlp = tmp_xml.name

            LOGGER.logger.debug(f"XML written to file {self.__xmlp}")

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """
        Exit point of the context
        :param exc_type: Type of the catched exception
        :type exc_type: Optional[Type[BaseException]]
        :param exc: Catched exception
        :type exc: Optional[BaseException]
        :param traceback: Traceback details
        :type traceback: Optional[TracebackType]
        """

        LOGGER.logger.debug("Destroying context for XML Validation")

        if os.path.isfile(self.__xmlp):
            os.remove(self.__xmlp)

            LOGGER.logger.debug(f"Deleted file {self.__xmlp}")

        if os.path.isfile(self.__xsdp):
            os.remove(self.__xsdp)

            LOGGER.logger.debug(f"Deleted file {self.__xsdp}")

    def is_valid(self) -> bool:
        """
        Check if the given XMl is a valid one
        """

        LOGGER.logger.debug("Validating XML")

        _xml: ElementTree = etree.parse(source=self.__xmlp)
        result = self.__xmlschema.validate(_xml)

        LOGGER.logger.debug(f"XML validation result: {result}")

        return result
