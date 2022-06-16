"""Create records related to one another via SQLAlchemy's ORM."""

import uuid

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
from ftl_python_lib.models.sql.message_category import ModelMessageCategory


class HelperMessageCategory:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for MessageCategory")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_message_category_object(self, search_result):
        message_category = ModelMessageCategory(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            name=search_result.name,
            description=search_result.description,
            created_by=search_result.created_by,
        )

        return message_category

    def get_by_id(self, id: str) -> ModelMessageCategory:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelMessageCategory)
                .filter(
                    and_(
                        ModelMessageCategory.id == id,
                        ModelMessageCategory.deleted_by.is_(None),
                        ModelMessageCategory.deleted_at.is_(None),
                    )
                )
                .first()
            )

            message_category = self._clone_message_category_object(search_result)

            return message_category
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message_category by id: {str(exc)}"
            )
            raise exc

    def get_by_name(self, name: str) -> ModelMessageCategory:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_message_category = (
                self.__session.query(ModelMessageCategory)
                .filter(
                    and_(
                        ModelMessageCategory.name == name,
                        ModelMessageCategory.deleted_by.is_(None),
                        ModelMessageCategory.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_message_category
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message_category by name: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str) -> ModelMessageCategory:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelMessageCategory)
                .filter(
                    and_(
                        ModelMessageCategory.reference_id == id,
                        ModelMessageCategory.deleted_by.is_(None),
                        ModelMessageCategory.deleted_at.is_(None),
                    )
                )
                .first()
            )

            message_category = self._clone_message_category_object(search_result)

            return message_category
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message_category by reference_id: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMessageCategory)
                .filter(
                    and_(
                        ModelMessageCategory.deleted_by.is_(None),
                        ModelMessageCategory.deleted_at.is_(None),
                    )
                )
                .order_by(asc(ModelMessageCategory.name))
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all message_category: {str(exc)}"
            )
            raise exc

    def update(
        self, message_category_update: ModelMessageCategory, owner_member_id: str
    ) -> ModelMessageCategory:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, message_category_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelMessageCategory(
                    id=new_id,
                    child_id=message_category_update.id,
                    reference_id=message_category_update.reference_id,
                    name=message_category_update.name,
                    description=message_category_update.description,
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
                f"Unexpected error when creating message_category: {exc}"
            )
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(
                f"Unexpected error when update message_category: {str(exc)}"
            )
            raise exc

    def create(
        self, message_category_new: ModelMessageCategory, owner_member_id: str
    ) -> ModelMessageCategory:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param message_category_new: New message_category record to create.
        :type message_category_new: ModelMessageCategory

        :return: Optional[ModelMessageCategory]
        """

        try:
            new_id = str(uuid.uuid4())
            message_category_new.id = new_id
            message_category_new.created_by = owner_member_id

            self.__session.add(message_category_new)
            self.__session.commit()

            member = self.get_by_id(new_id)

            return member
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(
                f"Unexpected error when creating message_category: {exc}"
            )
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelMessageCategory)
                .where(
                    and_(
                        ModelMessageCategory.reference_id == id,
                        ModelMessageCategory.deleted_by.is_(None),
                        ModelMessageCategory.deleted_at.is_(None),
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
                f"Unexpected error when delete a message_category: {str(exc)}"
            )
            raise exc
