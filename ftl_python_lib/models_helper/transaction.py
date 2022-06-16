"""Create records related to one another via SQLAlchemy's ORM."""

import json
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
from ftl_python_lib.models.sql.transaction import ModelTransaction
from ftl_python_lib.models_helper.microservice import HelperMicroservice


class HelperTransaction:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Transaction")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_transaction_object(self, search_result, raw: bool = False):
        microservices = []
        microservice_ids = json.loads(search_result.microservices)
        microservice_helper = HelperMicroservice(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )
        for microservice_id in microservice_ids:
            microservice = microservice_helper.get_by_reference_id(microservice_id)
            if raw:
                microservices.append(microservice.reference_id)
            else:
                microservices.append(
                    {"id": microservice.reference_id, "name": microservice.name}
                )

        transaction = ModelTransaction(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            type_id=search_result.type_id,
            name=search_result.name,
            description=search_result.description,
            active=search_result.active,
            microservices=microservices,
            created_by=search_result.created_by,
        )

        return transaction

    def get_by_id(self, id: str) -> ModelTransaction:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelTransaction)
                .filter(
                    and_(
                        ModelTransaction.id == id,
                        ModelTransaction.deleted_by.is_(None),
                        ModelTransaction.deleted_at.is_(None),
                    )
                )
                .first()
            )

            transaction = self._clone_transaction_object(search_result)

            return transaction
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get transaction by id: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str, raw: bool = False) -> ModelTransaction:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelTransaction)
                .filter(
                    and_(
                        ModelTransaction.reference_id == id,
                        ModelTransaction.deleted_by.is_(None),
                        ModelTransaction.deleted_at.is_(None),
                    )
                )
                .first()
            )

            transaction = self._clone_transaction_object(search_result, raw)

            return transaction
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get transaction by reference_id: {str(exc)}"
            )
            raise exc

    def get_by_name(self, name: str) -> ModelTransaction:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_transaction = (
                self.__session.query(ModelTransaction)
                .filter(
                    and_(
                        ModelTransaction.name == name,
                        ModelTransaction.deleted_by.is_(None),
                        ModelTransaction.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_transaction
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get transaction by name: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelTransaction)
                .filter(
                    and_(
                        ModelTransaction.deleted_by.is_(None),
                        ModelTransaction.deleted_at.is_(None),
                    )
                )
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all transaction: {str(exc)}"
            )
            raise exc

    def count(self):
        """
        Retrive count of all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelTransaction)
                .filter(
                    and_(
                        ModelTransaction.deleted_by.is_(None),
                        ModelTransaction.deleted_at.is_(None),
                    )
                )
                .count()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get count all transaction: {str(exc)}"
            )
            raise exc

    def count_active(self):
        """
        Retrive count of all active records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelTransaction)
                .filter(
                    and_(
                        ModelTransaction.active.is_(True),
                        ModelTransaction.deleted_by.is_(None),
                        ModelTransaction.deleted_at.is_(None),
                    )
                )
                .count()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get count all active transaction: {str(exc)}"
            )
            raise exc

    def update(
        self, transaction_update: ModelTransaction, owner_member_id: str
    ) -> ModelTransaction:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, transaction_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelTransaction(
                    id=new_id,
                    child_id=transaction_update.id,
                    reference_id=transaction_update.reference_id,
                    type_id=transaction_update.type_id,
                    name=transaction_update.name,
                    description=transaction_update.description,
                    active=transaction_update.active,
                    microservices=json.dumps(transaction_update.microservices),
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
            LOGGER.logger.error(f"Unexpected error when creating transaction: {exc}")
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(f"Unexpected error when update transaction: {str(exc)}")
            raise exc

    def create(
        self, transaction_new: ModelTransaction, owner_member_id: str
    ) -> ModelTransaction:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param transaction_new: New transaction record to create.
        :type transaction_new: ModelTransaction

        :return: Optional[ModelTransaction]
        """

        try:
            new_id = str(uuid.uuid4())
            transaction_new.id = new_id
            transaction_new.created_by = owner_member_id
            transaction_new.microservices = json.dumps(transaction_new.microservices)

            self.__session.add(transaction_new)
            self.__session.commit()

            member = self.get_by_id(new_id)

            return member
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(f"Unexpected error when creating transaction: {exc}")
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelTransaction)
                .where(
                    and_(
                        ModelTransaction.reference_id == id,
                        ModelTransaction.deleted_by.is_(None),
                        ModelTransaction.deleted_at.is_(None),
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
                f"Unexpected error when delete a transaction: {str(exc)}"
            )
            raise exc
