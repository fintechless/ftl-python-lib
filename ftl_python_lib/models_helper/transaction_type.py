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
from ftl_python_lib.models.sql.transaction_type import ModelTransactionType


class HelperTransactionType:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for TransactionType")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_transaction_type_object(self, search_result):
        transaction_type = ModelTransactionType(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            name=search_result.name,
            object_type=search_result.object_type,
            created_by=search_result.created_by,
        )

        return transaction_type

    def get_by_id(self, id: str) -> ModelTransactionType:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelTransactionType)
                .filter(
                    and_(
                        ModelTransactionType.id == id,
                        ModelTransactionType.deleted_by.is_(None),
                        ModelTransactionType.deleted_at.is_(None),
                    )
                )
                .first()
            )

            transaction_type = self._clone_transaction_type_object(search_result)

            return transaction_type
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get transaction_type by id: {str(exc)}"
            )
            raise exc

    def get_by_name(self, name: str) -> ModelTransactionType:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_transaction_type = (
                self.__session.query(ModelTransactionType)
                .filter(
                    and_(
                        ModelTransactionType.name == name,
                        ModelTransactionType.deleted_by.is_(None),
                        ModelTransactionType.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_transaction_type
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get transaction_type by name: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str) -> ModelTransactionType:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelTransactionType)
                .filter(
                    and_(
                        ModelTransactionType.reference_id == id,
                        ModelTransactionType.deleted_by.is_(None),
                        ModelTransactionType.deleted_at.is_(None),
                    )
                )
                .first()
            )

            transaction_type = self._clone_transaction_type_object(search_result)

            return transaction_type
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get transaction_type by reference_id: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelTransactionType)
                .filter(
                    and_(
                        ModelTransactionType.deleted_by.is_(None),
                        ModelTransactionType.deleted_at.is_(None),
                    )
                )
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all transaction_type: {str(exc)}"
            )
            raise exc

    def update(
        self, transaction_type_update: ModelTransactionType, owner_member_id: str
    ) -> ModelTransactionType:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, transaction_type_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelTransactionType(
                    id=new_id,
                    child_id=transaction_type_update.id,
                    reference_id=transaction_type_update.reference_id,
                    name=transaction_type_update.name,
                    object_type=transaction_type_update.object_type,
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
                f"Unexpected error when creating transaction_type: {exc}"
            )
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(
                f"Unexpected error when update transaction_type: {str(exc)}"
            )
            raise exc

    def create(
        self, transaction_type_new: ModelTransactionType, owner_member_id: str
    ) -> ModelTransactionType:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param transaction_type_new: New transaction_type record to create.
        :type transaction_type_new: ModelTransactionType

        :return: Optional[ModelTransactionType]
        """

        try:
            new_id = str(uuid.uuid4())
            transaction_type_new.id = new_id
            transaction_type_new.created_by = owner_member_id

            self.__session.add(transaction_type_new)
            self.__session.commit()

            member = self.get_by_id(new_id)

            return member
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(
                f"Unexpected error when creating transaction_type: {exc}"
            )
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelTransactionType)
                .where(
                    and_(
                        ModelTransactionType.reference_id == id,
                        ModelTransactionType.deleted_by.is_(None),
                        ModelTransactionType.deleted_at.is_(None),
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
                f"Unexpected error when delete a transaction_type: {str(exc)}"
            )
            raise exc
