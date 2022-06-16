"""Create records related to one another via SQLAlchemy's ORM."""

import uuid

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import SQLAlchemyError

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.context.session import SessionContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.models.sql.message_target import ModelMessageTarget


class HelperMessageTarget:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for MessageTarget")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_message_target_object(self, search_result):
        message_target = ModelMessageTarget(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            name=search_result.name,
            type=search_result.type,
            created_by=search_result.created_by,
        )

        return message_target

    def get_by_id(self, id: str) -> ModelMessageTarget:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelMessageTarget)
                .filter(
                    and_(
                        ModelMessageTarget.id == id,
                        ModelMessageTarget.deleted_by.is_(None),
                        ModelMessageTarget.deleted_at.is_(None),
                    )
                )
                .first()
            )

            message_target = self._clone_message_target_object(search_result)

            return message_target
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message_target by id: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str) -> ModelMessageTarget:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelMessageTarget)
                .filter(
                    and_(
                        ModelMessageTarget.reference_id == id,
                        ModelMessageTarget.deleted_by.is_(None),
                        ModelMessageTarget.deleted_at.is_(None),
                    )
                )
                .first()
            )

            message_target = self._clone_message_target_object(search_result)

            return message_target
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message_target by reference_id: {str(exc)}"
            )
            raise exc

    def get_by_name(self, name: str) -> ModelMessageTarget:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_message_target = (
                self.__session.query(ModelMessageTarget)
                .filter(
                    and_(
                        ModelMessageTarget.name == name,
                        ModelMessageTarget.deleted_by.is_(None),
                        ModelMessageTarget.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_message_target
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message_target by name: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMessageTarget)
                .filter(
                    and_(
                        ModelMessageTarget.deleted_by.is_(None),
                        ModelMessageTarget.deleted_at.is_(None),
                    )
                )
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all message_target: {str(exc)}"
            )
            raise exc

    def update(
        self, message_target_update: ModelMessageTarget, owner_member_id: str
    ) -> ModelMessageTarget:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, message_target_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelMessageTarget(
                    id=new_id,
                    child_id=message_target_update.id,
                    reference_id=message_target_update.reference_id,
                    name=message_target_update.name,
                    type=message_target_update.type,
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
            LOGGER.logger.error(f"Unexpected error when creating message_target: {exc}")
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(
                f"Unexpected error when update message_target: {str(exc)}"
            )
            raise exc

    def create(
        self, message_target_new: ModelMessageTarget, owner_member_id: str
    ) -> ModelMessageTarget:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param message_target_new: New message_target record to create.
        :type message_target_new: ModelMessageTarget

        :return: Optional[ModelMessageTarget]
        """

        try:
            new_id = str(uuid.uuid4())
            message_target_new.id = new_id
            message_target_new.created_by = owner_member_id

            self.__session.add(message_target_new)
            self.__session.commit()

            member = self.get_by_id(new_id)

            return member
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(f"Unexpected error when creating message_target: {exc}")
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelMessageTarget)
                .where(
                    and_(
                        ModelMessageTarget.reference_id == id,
                        ModelMessageTarget.deleted_by.is_(None),
                        ModelMessageTarget.deleted_at.is_(None),
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
                f"Unexpected error when delete a message_target: {str(exc)}"
            )
            raise exc
