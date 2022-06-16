"""Create records related to one another via SQLAlchemy's ORM."""

import uuid

from bs4 import BeautifulSoup
from sqlalchemy import and_
from sqlalchemy import asc
from sqlalchemy import func
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import SQLAlchemyError

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.context.session import SessionContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.models.sql.message_definition import ModelMessageDefinition
from ftl_python_lib.utils.to_str import bytes_to_str


class HelperMessageDefinition:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for MessageDefinition")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_message_definition_object(self, search_result):
        message_definition = ModelMessageDefinition(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            name=search_result.name,
            type=search_result.type,
            activated_at=search_result.activated_at,
            message_id=search_result.message_id,
            xsd_tag=search_result.xsd_tag,
            annotation_name=search_result.annotation_name,
            annotation_definition=search_result.annotation_definition,
            parent_id=search_result.parent_id,
            level=search_result.level,
            is_leaf=search_result.is_leaf,
            target_column=search_result.target_column,
            target_type=search_result.target_type,
            element_index=search_result.element_index,
            created_by=search_result.created_by,
        )

        return message_definition

    def get_by_id(self, id: str) -> ModelMessageDefinition:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelMessageDefinition)
                .filter(
                    and_(
                        ModelMessageDefinition.id == id,
                        ModelMessageDefinition.deleted_by.is_(None),
                        ModelMessageDefinition.deleted_at.is_(None),
                    )
                )
                .first()
            )

            message_definition = self._clone_message_definition_object(search_result)

            return message_definition
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message_definition by id: {str(exc)}"
            )
            raise exc

    def get_by_name(self, name: str) -> ModelMessageDefinition:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_message_definition = (
                self.__session.query(ModelMessageDefinition)
                .filter(
                    and_(
                        ModelMessageDefinition.name == name,
                        ModelMessageDefinition.deleted_by.is_(None),
                        ModelMessageDefinition.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_message_definition
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message_definition by name: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str) -> ModelMessageDefinition:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelMessageDefinition)
                .filter(
                    and_(
                        ModelMessageDefinition.reference_id == id,
                        ModelMessageDefinition.deleted_by.is_(None),
                        ModelMessageDefinition.deleted_at.is_(None),
                    )
                )
                .first()
            )

            message_definition = self._clone_message_definition_object(search_result)

            return message_definition
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message_definition by reference_id: {str(exc)}"
            )
            raise exc

    def get_by_message_id(self, message_id: str):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMessageDefinition)
                .filter(
                    and_(
                        ModelMessageDefinition.message_id == message_id,
                        ModelMessageDefinition.deleted_by.is_(None),
                        ModelMessageDefinition.deleted_at.is_(None),
                    )
                )
                .order_by(asc(ModelMessageDefinition.element_index))
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all message_definition: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMessageDefinition)
                .filter(ModelMessageDefinition.deleted_by.is_(None))
                .filter(ModelMessageDefinition.deleted_at.is_(None))
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all message_definition: {str(exc)}"
            )
            raise exc

    def update(
        self, message_definition_update: ModelMessageDefinition, owner_member_id: str
    ) -> ModelMessageDefinition:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, message_definition_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelMessageDefinition(
                    id=new_id,
                    child_id=message_definition_update.id,
                    reference_id=message_definition_update.reference_id,
                    name=message_definition_update.name,
                    type=message_definition_update.type,
                    activated_at=message_definition_update.activated_at,
                    message_id=message_definition_update.message_id,
                    xsd_tag=message_definition_update.xsd_tag,
                    annotation_name=message_definition_update.annotation_name,
                    annotation_definition=message_definition_update.annotation_definition,
                    parent_id=message_definition_update.parent_id,
                    level=message_definition_update.level,
                    is_leaf=message_definition_update.is_leaf,
                    target_column=message_definition_update.target_column,
                    target_type=message_definition_update.target_type,
                    element_index=message_definition_update.element_index,
                    created_by=owner_member_id,
                )
            )
            self.__session.commit()

            return self.get_by_id(new_id)
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
            LOGGER.logger.error(
                f"Unexpected error when creating message_definition: {exc}"
            )
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(
                f"Unexpected error when update message_definition: {str(exc)}"
            )
            raise exc

    def create(
        self, message_definition_new: ModelMessageDefinition, owner_member_id: str
    ) -> ModelMessageDefinition:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param message_definition_new: New message_definition record to create.
        :type message_definition_new: ModelMessageDefinition

        :return: Optional[ModelMessageDefinition]
        """

        try:
            new_id = str(uuid.uuid4())
            message_definition_new.id = new_id
            message_definition_new.created_by = owner_member_id

            self.__session.add(message_definition_new)
            self.__session.commit()

            member = self.get_by_id(new_id)

            return member
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(
                f"Unexpected error when creating message_definition: {exc}"
            )
            raise exc

    def create_from_content(
        self, owner_member_id: str, reference_id: str, content: bytes
    ) -> ModelMessageDefinition:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param message_definition_new: New message_definition record to create.
        :type message_definition_new: ModelMessageDefinition

        :return: Optional[ModelMessageDefinition]
        """

        try:
            soup = BeautifulSoup(bytes_to_str(src=content), "xml")

            LOGGER.logger.debug("[INFO] Message definitions are beeing generated")
            message_definition = []
            tree = self._get_tree(soup)
            element_index = 0
            for item in tree:
                message_definition.append(
                    ModelMessageDefinition(
                        id=item["id"],
                        message_id=reference_id,
                        xsd_tag=item["xsd_tag"],
                        name=item["name"],
                        type=item["type"],
                        annotation_name=item["annotation_name"],
                        annotation_definition=item["annotation_definition"],
                        parent_id=item["parent_id"],
                        level=item["level"],
                        is_leaf=item["is_leaf"],
                        target_column=item["target_column"],
                        target_type=item["target_type"],
                        element_index=element_index,
                        created_by=owner_member_id,
                    )
                )
                element_index = element_index + 1
            self.__session.add_all(message_definition)
            self.__session.commit()
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(
                f"Unexpected error when creating message_definition: {exc}"
            )
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelMessageDefinition)
                .where(
                    and_(
                        ModelMessageDefinition.reference_id == id,
                        ModelMessageDefinition.deleted_by.is_(None),
                        ModelMessageDefinition.deleted_at.is_(None),
                    )
                )
                .values(
                    deleted_by=owner_member_id,
                    deleted_at=func.now(),
                )
                .execution_options(synchronize_session="fetch")
            )

            self.__session.execute(stmt)
            self.__session.commit()
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when delete a message_definition: {str(exc)}"
            )
            raise exc

    def delete_by_message_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelMessageDefinition)
                .where(
                    and_(
                        ModelMessageDefinition.message_id == id,
                        ModelMessageDefinition.deleted_by.is_(None),
                        ModelMessageDefinition.deleted_at.is_(None),
                    )
                )
                .values(
                    deleted_by=owner_member_id,
                    deleted_at=func.now(),
                )
                .execution_options(synchronize_session="fetch")
            )

            self.__session.execute(stmt)
            self.__session.commit()
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when delete a message_definition: {str(exc)}"
            )
            raise exc

    def _get_tree(
        self,
        soup,
        element_name: str = "Document",
        element_type: str = "Document",
        parent_id: str = str(uuid.uuid4()),
        level: int = 0,
    ):
        result = []

        element = soup.find("xs:element", {"name": element_name, "type": element_type})

        if element is not None:
            _name = element.find("xs:documentation", {"source": "Name"})
            if _name is not None:
                _name = _name.get_text()

            _def = element.find("xs:documentation", {"source": "Definition"})
            if _def is not None:
                _def = _def.get_text()

            _new_id = str(uuid.uuid4())
            result.append(
                {
                    "id": _new_id,
                    "xsd_tag": "element",
                    "name": element["name"],
                    "type": element["type"],
                    "annotation_name": _name,
                    "annotation_definition": _def,
                    "parent_id": parent_id,
                    "level": level,
                    "is_leaf": False,
                    "target_column": "",
                    "target_type": "",
                }
            )
            parent_id = _new_id

            last = len(result) - 1

            complex_type = soup.find("xs:complexType", {"name": element["type"]})
            if complex_type is not None:
                search = complex_type.find("xs:sequence")

                if search.is_(None):
                    search = complex_type.find("xs:simpleContent")

                if search.is_(None):
                    search = complex_type.find("xs:choice")

                children = search.find_all("xs:element")

                if len(children) > 0:
                    for i in range(len(children)):
                        result = result + self._get_tree(
                            soup,
                            children[i]["name"],
                            children[i]["type"],
                            parent_id,
                            level + 1,
                        )
                else:
                    result[last]["is_leaf"] = True
            else:
                result[last]["is_leaf"] = True

        return result
