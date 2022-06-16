"""Create records related to one another via SQLAlchemy's ORM."""

import re
from types import NoneType
from zipfile import ZipFile

import requests
import wget
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import SQLAlchemyError

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.context.session import SessionContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.models.sql.message import ModelMessage
from ftl_python_lib.models.sql.message_category import ModelMessageCategory
from ftl_python_lib.models_helper.message import HelperMessage
from ftl_python_lib.models_helper.message_category import HelperMessageCategory
from ftl_python_lib.utils.to_bytes import UtilsConversionsToBytes


class HelperMessageParser:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Message")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def parser(self, owner_member_id: str):
        """
        Message Parser.
        """
        _types = {}
        _markdown = "# Message Definitions"

        try:
            for page in [0, 1]:
                response = requests.get(
                    f"{self.__environ_context.message_definitions_host}?page={page}"
                )
                soup = BeautifulSoup(response.text, "html.parser")

                _id = soup.find_all(
                    "div", class_="catalog-col__main d-flex align-items-center"
                )
                for key, value in enumerate(_id):
                    _types[value.find("span").text.strip()] = value.find(
                        "h5"
                    ).text.strip()

                LOGGER.logger.debug("[INFO] Message types are processed")

                _id = soup.find_all("div", class_="catalog-sub catalog-sub__message-id")
                _desc = soup.find_all(
                    "div", class_="catalog-sub catalog-sub__message-name"
                )
                _org = soup.find_all(
                    "div", class_="catalog-sub catalog-sub__organisation"
                )
                _href = soup.find_all(
                    "a",
                    href=True,
                    class_="btn btn-download d-inline-flex align-items-center has-tooltip",
                )

                _key = 0
                for key, value in enumerate(_id):
                    msg = value.text.strip()
                    if msg == "Message ID (scheme)":
                        _key += 1

                        _markdown = f"{_markdown}\n\n## Category\n"
                    else:
                        self._add_message(
                            owner_member_id,
                            key,
                            _desc,
                            _org,
                            _href,
                            _key,
                            msg,
                        )
        except InvalidRequestError as exc:
            self.__session.rollback()
            LOGGER.logger.error(exc)
            raise exc
        except IntegrityError as exc:
            self.__session.rollback()
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            self.__session.rollback()
            LOGGER.logger.error(f"Unexpected error when creating message: {exc}")
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(f"Unexpected error when update message: {str(exc)}")
            raise exc

    def _add_message(self, owner_member_id, key, _desc, _org, _href, _key, msg):
        desc = _desc[key].text.strip()
        desc = desc.replace("AgentCA", "AgentCorporateAction")
        desc = desc.replace("ATM", "AutomatedTellerMachine")
        desc = desc.replace("CCP", "CentralCounterParty")
        desc = desc.replace("FI", "FinancialInstitution")
        desc = desc.replace("POI", "PointOfInteraction")
        desc = desc.replace("POS", "PointOfSale")
        desc = re.sub(r"(?<!^)(?=[A-Z])", " ", desc)

        _message_category_helper = HelperMessageCategory(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )
        unique_type: str = msg[0:4]
        version_major: str = msg[5:8]
        version_minor: str = msg[9:12]
        version_patch: str = msg[13:15]

        _message_category = _message_category_helper.get_by_name(name=unique_type)

        if isinstance(_message_category, NoneType):
            _message_category = _message_category_helper.create(
                message_category_new=ModelMessageCategory(
                    name=msg[0:4], description=desc
                ),
                owner_member_id=owner_member_id,
            )

        href = _href[key - _key]["href"]
        url = f"https://www.iso20022.org{href}"

        _message_helper = HelperMessage(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )
        _all_messages = _message_helper.get_all_unique_keys()

        if msg not in _all_messages:
            # response = requests.get(url)
            try:
                filename = wget.download(url)
                _final_file_name = filename
                if filename.endswith(".zip"):
                    with ZipFile(filename, "r") as _zip_object:
                        _final_file_name = filename.replace(".zip", ".xsd")
                        _zip_object.extract(_final_file_name)
                file = open(_final_file_name, "r")
                _message_helper.create(
                    message_new=ModelMessage(
                        unique_key=f"{unique_type}.{version_major}",
                        unique_type=unique_type,
                        version_major=version_major,
                        version_minor=version_minor,
                        version_patch=version_patch,
                        description=desc,
                        org=_org[key].text.strip(),
                        url=url,
                        active=False,
                        category_id=_message_category.reference_id,
                    ),
                    owner_member_id=owner_member_id,
                    content=UtilsConversionsToBytes.str_to_bytes(file.read()),
                )
            except Exception as exc:
                LOGGER.logger.error(
                    f"Unexpected error when download message {url}: {str(exc)}"
                )
