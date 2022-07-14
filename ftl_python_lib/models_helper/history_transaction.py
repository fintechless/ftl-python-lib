"""Create records related to one another via SQLAlchemy's ORM."""


import uuid

from sqlalchemy import CHAR
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import cast

from ftl_python_lib.constants.models.transaction import ConstantsTransactionStatus
from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.context.session import SessionContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.models.sql.history_transaction import ModelHistoryTransaction
from ftl_python_lib.models.sql.response import ModelResponse


class HelperHistoryTransaction:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for HistoryTransaction")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def create(
        self, history_transaction_new: ModelHistoryTransaction, owner_member_id: str
    ) -> ModelHistoryTransaction:
        """
        Create new HistoryTransaction
        """

        try:
            history_transaction_new.id = str(uuid.uuid4())
            history_transaction_new.created_by = owner_member_id

            self.__session.add(history_transaction_new)
            self.__session.commit()

            return history_transaction_new
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(
                f"Unexpected error when creating history transaction: {exc}"
            )
            raise exc

    def get_last_execution(self):
        """
        Retrive last 10 execution.

        :return: Session
        """

        try:
            return (
                self.__session.query(
                    cast(ModelHistoryTransaction.requested_at, CHAR),
                    ModelHistoryTransaction.message_type,
                    ModelHistoryTransaction.status,
                )
                .filter(
                    and_(
                        (
                            (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.RELEASED.value
                            )
                            | (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.REJECTED.value
                            )
                        ),
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                    )
                )
                .order_by(ModelHistoryTransaction.requested_at)
                .limit(10)
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get last 10 execution: {str(exc)}"
            )
            raise exc

    def get_last_rejection(self):
        """
        Retrive last 10 rejection.

        :return: Session
        """

        try:
            return (
                self.__session.query(
                    cast(ModelHistoryTransaction.requested_at, CHAR),
                    ModelHistoryTransaction.message_type,
                    ModelHistoryTransaction.response_code,
                    ModelHistoryTransaction.response_message,
                    ModelResponse.description,
                )
                .outerjoin(
                    ModelResponse,
                    ModelHistoryTransaction.response_code
                    == ModelResponse.response_code,
                )
                .filter(
                    and_(
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                        ModelHistoryTransaction.status
                        == ConstantsTransactionStatus.REJECTED.value,
                    )
                )
                .order_by(ModelHistoryTransaction.requested_at)
                .limit(10)
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get last 10 rejection: {str(exc)}"
            )
            raise exc

    def get_volume_by_hour(self, from_date: str, to_date: str):
        """
        Retrive all volume by hour.

        :return: Session
        """

        try:
            return (
                self.__session.query(
                    func.date_format(ModelHistoryTransaction.requested_at, "%H"),
                    ModelHistoryTransaction.status,
                    func.count(ModelHistoryTransaction.id),
                )
                .filter(
                    and_(
                        (
                            (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.RELEASED.value
                            )
                            | (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.REJECTED.value
                            )
                        ),
                        ModelHistoryTransaction.requested_at >= from_date,
                        ModelHistoryTransaction.requested_at <= to_date,
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                    )
                )
                .group_by(func.date_format(ModelHistoryTransaction.requested_at, "%H"))
                .group_by(ModelHistoryTransaction.status)
            )
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get volume by hour: {str(exc)}")
            raise exc

    def get_volume_by_day(self, from_date: str, to_date: str):
        """
        Retrive all volume by day.

        :return: Session
        """

        try:
            return (
                self.__session.query(
                    func.date_format(ModelHistoryTransaction.requested_at, "%d"),
                    ModelHistoryTransaction.status,
                    func.count(ModelHistoryTransaction.id),
                )
                .filter(
                    and_(
                        (
                            (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.RELEASED.value
                            )
                            | (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.REJECTED.value
                            )
                        ),
                        ModelHistoryTransaction.requested_at >= from_date,
                        ModelHistoryTransaction.requested_at <= to_date,
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                    )
                )
                .group_by(func.date_format(ModelHistoryTransaction.requested_at, "%d"))
                .group_by(ModelHistoryTransaction.status)
            )
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get volume by day: {str(exc)}")
            raise exc

    def get_currency_by_hour(self, from_date: str, to_date: str):
        """
        Retrive all currency by hour.

        :return: Session
        """

        try:
            return (
                self.__session.query(
                    func.date_format(ModelHistoryTransaction.requested_at, "%H"),
                    ModelHistoryTransaction.status,
                    func.sum(ModelHistoryTransaction.amount),
                )
                .filter(
                    and_(
                        (
                            (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.RELEASED.value
                            )
                            | (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.REJECTED.value
                            )
                        ),
                        ModelHistoryTransaction.requested_at >= from_date,
                        ModelHistoryTransaction.requested_at <= to_date,
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                        ModelHistoryTransaction.amount.isnot(None),
                    )
                )
                .group_by(func.date_format(ModelHistoryTransaction.requested_at, "%H"))
                .group_by(ModelHistoryTransaction.status)
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get currency by hour: {str(exc)}"
            )
            raise exc

    def get_currency_by_day(self, from_date: str, to_date: str):
        """
        Retrive all currency by day.

        :return: Session
        """

        try:
            return (
                self.__session.query(
                    func.date_format(ModelHistoryTransaction.requested_at, "%d"),
                    ModelHistoryTransaction.status,
                    func.sum(ModelHistoryTransaction.amount),
                )
                .filter(
                    and_(
                        (
                            (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.RELEASED.value
                            )
                            | (
                                ModelHistoryTransaction.status
                                == ConstantsTransactionStatus.REJECTED.value
                            )
                        ),
                        ModelHistoryTransaction.requested_at >= from_date,
                        ModelHistoryTransaction.requested_at <= to_date,
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                        ModelHistoryTransaction.amount.isnot(None),
                    )
                )
                .group_by(func.date_format(ModelHistoryTransaction.requested_at, "%d"))
                .group_by(ModelHistoryTransaction.status)
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get currency by day: {str(exc)}"
            )
            raise exc

    def get_volume_accepted(self, from_date: str, to_date: str):
        """
        Retrive volume accepted by date.

        :return: Session
        """

        try:
            volume_accepted = (
                self.__session.query(func.count(ModelHistoryTransaction.id))
                .filter(
                    and_(
                        ModelHistoryTransaction.status
                        == ConstantsTransactionStatus.RELEASED.value,
                        ModelHistoryTransaction.requested_at >= from_date,
                        ModelHistoryTransaction.requested_at <= to_date,
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                    )
                )
                .scalar()
                or 0
            )

            return volume_accepted
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get volume accepted by date: {str(exc)}"
            )
            raise exc

    def get_volume_rejected(self, from_date: str, to_date: str):
        """
        Retrive volume rejected by date.

        :return: Session
        """

        try:
            volume_accepted = (
                self.__session.query(func.count(ModelHistoryTransaction.id))
                .filter(
                    and_(
                        ModelHistoryTransaction.status
                        == ConstantsTransactionStatus.REJECTED.value,
                        ModelHistoryTransaction.requested_at >= from_date,
                        ModelHistoryTransaction.requested_at <= to_date,
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                    )
                )
                .scalar()
                or 0
            )

            return volume_accepted
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get volume rejected by date: {str(exc)}"
            )
            raise exc

    def get_total_volume_rejected(self):
        """
        Retrive volume rejected.

        :return: Session
        """

        try:
            volume_accepted = (
                self.__session.query(func.count(ModelHistoryTransaction.id))
                .filter(
                    and_(
                        ModelHistoryTransaction.status
                        == ConstantsTransactionStatus.REJECTED.value,
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                    )
                )
                .scalar()
                or 0
            )

            return volume_accepted
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get volume rejected: {str(exc)}"
            )
            raise exc

    def get_total_volume(self):
        """
        Retrive volume.

        :return: Session
        """

        try:
            volume_accepted = (
                self.__session.query(func.count(ModelHistoryTransaction.id))
                .filter(
                    and_(
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                    )
                )
                .scalar()
                or 0
            )

            return volume_accepted
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get volume: {str(exc)}")
            raise exc

    def get_currency_accepted(self, from_date: str, to_date: str):
        """
        Retrive currency accepted by date.

        :return: Session
        """

        try:
            currency_accepted = (
                self.__session.query(func.sum(ModelHistoryTransaction.amount))
                .filter(
                    and_(
                        ModelHistoryTransaction.status
                        == ConstantsTransactionStatus.RELEASED.value,
                        ModelHistoryTransaction.requested_at >= from_date,
                        ModelHistoryTransaction.requested_at <= to_date,
                        ModelHistoryTransaction.amount.isnot(None),
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                    )
                )
                .scalar()
                or 0
            )

            return currency_accepted
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get currency accepted by date: {str(exc)}"
            )
            raise exc

    def get_currency_rejected(self, from_date: str, to_date: str):
        """
        Retrive currency accepted by date.

        :return: Session
        """

        try:
            currency_accepted = (
                self.__session.query(func.sum(ModelHistoryTransaction.amount))
                .filter(
                    and_(
                        ModelHistoryTransaction.status
                        == ConstantsTransactionStatus.REJECTED.value,
                        ModelHistoryTransaction.requested_at >= from_date,
                        ModelHistoryTransaction.requested_at <= to_date,
                        ModelHistoryTransaction.amount.isnot(None),
                        ModelHistoryTransaction.deleted_by.is_(None),
                        ModelHistoryTransaction.deleted_at.is_(None),
                    )
                )
                .scalar()
                or 0
            )

            return currency_accepted
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get currency accepted by date: {str(exc)}"
            )
            raise exc
