"""Create records related to one another via SQLAlchemy's ORM."""

import uuid
import os

from sqlalchemy import and_
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import SQLAlchemyError

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.headers import HeadersContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.context.session import SessionContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.core.providers.aws.s3 import ProviderS3
from ftl_python_lib.models.sql.message import ModelMessage
from ftl_python_lib.models_helper.message_definition import HelperMessageDefinition
from ftl_python_lib.typings.providers.aws.s3object import TypeS3Object


class HelperMessage:
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
        self.__provider_s3: ProviderS3 = ProviderS3(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )

    def _clone_message_object(self, search_result):
        message = ModelMessage(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            category_id=search_result.category_id,
            unique_key=search_result.unique_key,
            description=search_result.description,
            org=search_result.org,
            url=search_result.url,
            storage_path=search_result.storage_path,
            unique_type=search_result.unique_type,
            version_major=search_result.version_major,
            version_minor=search_result.version_minor,
            version_patch=search_result.version_patch,
            active=search_result.active,
            created_by=search_result.created_by,
        )

        return message

    def get_by_id(self, id: str) -> ModelMessage:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelMessage)
                .filter(
                    and_(
                        ModelMessage.id == id,
                        ModelMessage.deleted_by.is_(None),
                        ModelMessage.deleted_at.is_(None),
                    )
                )
                .first()
            )

            message = self._clone_message_object(search_result)

            return message
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get message by id: {str(exc)}")
            raise exc

    def get_reference_id(self, id: str) -> ModelMessage:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMessage)
                .filter(
                    and_(
                        ModelMessage.reference_id == id,
                        ModelMessage.deleted_by.is_(None),
                        ModelMessage.deleted_at.is_(None),
                    )
                )
                .first()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message by reference_id: {str(exc)}"
            )
            raise exc

    def get_by_key(
        self,
        unique_type: str,
        version_major: str,
        version_minor: str,
        version_patch: str,
    ) -> ModelMessage:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_message = (
                self.__session.query(ModelMessage)
                .filter(
                    and_(
                        ModelMessage.unique_type == unique_type,
                        ModelMessage.version_major == version_major,
                        ModelMessage.version_minor == version_minor,
                        ModelMessage.version_patch == version_patch,
                        ModelMessage.deleted_by.is_(None),
                        ModelMessage.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_message
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message by unique_key: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str) -> ModelMessage:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelMessage)
                .filter(
                    and_(
                        ModelMessage.reference_id == id,
                        ModelMessage.deleted_by.is_(None),
                        ModelMessage.deleted_at.is_(None),
                    )
                )
                .first()
            )

            message = self._clone_message_object(search_result)

            return message
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get message by reference_id: {str(exc)}"
            )
            raise exc

    def get_all_by_category_id(self, category_id: str):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMessage)
                .filter(
                    and_(
                        ModelMessage.category_id == category_id,
                        ModelMessage.deleted_by.is_(None),
                        ModelMessage.deleted_at.is_(None),
                    )
                )
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get all message: {str(exc)}")
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            messages = []
            message_keys = []
            message_list = (
                self.__session.query(ModelMessage)
                .filter(
                    and_(
                        ModelMessage.deleted_by.is_(None),
                        ModelMessage.deleted_at.is_(None),
                    )
                )
                .order_by(asc(ModelMessage.unique_type))
                .order_by(asc(ModelMessage.version_major))
                .order_by(desc(ModelMessage.version_minor))
                .order_by(desc(ModelMessage.version_patch))
                .all()
            )

            for message in message_list:
                if message.unique_key not in message_keys:
                    message_keys.append(message.unique_key)
                    messages.append(message)

            return messages
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get all message: {str(exc)}")
            raise exc

    def get_all_active(self):
        """
        Retrive all active records.

        :return: Session
        """

        try:
            messages = []
            message_keys = []
            message_list = (
                self.__session.query(ModelMessage)
                .filter(
                    and_(
                        ModelMessage.active.is_(True),
                        ModelMessage.deleted_by.is_(None),
                        ModelMessage.deleted_at.is_(None),
                    )
                )
                .order_by(asc(ModelMessage.unique_type))
                .order_by(asc(ModelMessage.version_major))
                .order_by(desc(ModelMessage.version_minor))
                .order_by(desc(ModelMessage.version_patch))
                .all()
            )

            for message in message_list:
                if message.unique_key not in message_keys:
                    message_keys.append(message.unique_key)
                    messages.append(message)

            return messages
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all active message: {str(exc)}"
            )
            raise exc

    def get_all_unique_keys(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            unique_keys = []
            messages = (
                self.__session.query(ModelMessage)
                .filter(
                    and_(
                        ModelMessage.deleted_by.is_(None),
                        ModelMessage.deleted_at.is_(None),
                    )
                )
                .all()
            )

            for item in messages:
                unique_keys.append(
                    f"{item.unique_type}.{item.version_major}.{item.version_minor}.{item.version_patch}"
                )

            return unique_keys
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get all message: {str(exc)}")
            raise exc

    def update(
        self, message_update: ModelMessage, owner_member_id: str, content: bytes
    ) -> ModelMessage:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, message_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelMessage(
                    id=new_id,
                    child_id=message_update.id,
                    reference_id=message_update.reference_id,
                    category_id=message_update.category_id,
                    unique_key=message_update.unique_key,
                    description=message_update.description,
                    org=message_update.org,
                    url=message_update.url,
                    storage_path=message_update.storage_path,
                    unique_type=message_update.unique_type,
                    version_major=message_update.version_major,
                    version_minor=message_update.version_minor,
                    version_patch=message_update.version_patch,
                    active=message_update.active,
                    created_by=owner_member_id,
                )
            )
            self.__session.commit()

            message = self.get_by_id(new_id)

            if content is not None:
                message_definition = HelperMessageDefinition(
                    request_context=self.__request_context,
                    environ_context=self.__environ_context,
                )
                message_definition.delete_by_message_id(
                    owner_member_id, message.reference_id
                )
                message_definition.create_from_content(
                    owner_member_id, message.reference_id, content
                )

            return message
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

    def create(
        self, message_new: ModelMessage, owner_member_id: str, content: bytes
    ) -> ModelMessage:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param message_new: New message record to create.
        :type message_new: ModelMessage

        :return: Optional[ModelMessage]
        """

        try:
            new_id = str(uuid.uuid4())
            message_new.id = new_id
            message_new.created_by = owner_member_id
            message_new.storage_path = os.path.join(
                "schema",
                "xsd",
                f"{new_id}_"
                + f"{message_new.unique_type}.{message_new.version_major}"
                + f".{message_new.version_minor}.{message_new.version_patch}"
                + ".xsd",
            )

            self.__session.add(message_new)
            self.__session.commit()

            message = self.get_by_id(new_id)

            self.__provider_s3.put_object(
                object=TypeS3Object(
                    bucket=self.__environ_context.runtime_bucket,
                    key=message.storage_path,
                    body=content,
                )
            )
            message_definition = HelperMessageDefinition(
                request_context=self.__request_context,
                environ_context=self.__environ_context,
            )
            message_definition.create_from_content(
                owner_member_id, message.reference_id, content
            )

            return message
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(f"Unexpected error when creating message: {exc}")
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelMessage)
                .where(
                    and_(
                        ModelMessage.reference_id == id,
                        ModelMessage.deleted_by.is_(None),
                        ModelMessage.deleted_at.is_(None),
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
            LOGGER.logger.error(f"Unexpected error when delete a message: {str(exc)}")
            raise exc
