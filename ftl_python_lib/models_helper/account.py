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
from ftl_python_lib.models.sql.account import ModelAccount
from ftl_python_lib.models_helper.member import HelperMember


class HelperAccount:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Account")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_account_object(self, search_result):
        account = ModelAccount(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            name=search_result.name,
            email=search_result.email,
            description=search_result.description,
            website=search_result.website,
            member=search_result.member,
            created_by=search_result.created_by,
        )

        return account

    def get_first(self) -> ModelAccount:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelAccount)
                .filter(
                    and_(
                        ModelAccount.deleted_by.is_(None),
                        ModelAccount.deleted_at.is_(None),
                    )
                )
                .first()
            )

            account = self._clone_account_object(search_result)

            self._get_member_list(account)

            return account
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get first account: {str(exc)}")
            raise exc

    def get_by_id(self, id: str) -> ModelAccount:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelAccount)
                .filter(
                    and_(
                        ModelAccount.id == id,
                        ModelAccount.deleted_by.is_(None),
                        ModelAccount.deleted_at.is_(None),
                    )
                )
                .first()
            )

            account = self._clone_account_object(search_result)

            self._get_member_list(account)

            return account
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get account by id: {str(exc)}")
            raise exc

    def get_reference_id(self, id: str) -> ModelAccount:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelAccount)
                .filter(
                    and_(
                        ModelAccount.reference_id == id,
                        ModelAccount.deleted_by.is_(None),
                        ModelAccount.deleted_at.is_(None),
                    )
                )
                .first()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get member by reference_id: {str(exc)}"
            )
            raise exc

    def _get_member_list(self, account):
        member_helper = HelperMember(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )
        member_list = member_helper.get_all()
        members = []
        for member in member_list:
            members.append(
                {
                    "id": member.reference_id,
                    "email": member.email,
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                    "avatar": member.avatar,
                    "role": member.role,
                }
            )

        account.member = members

    def update(
        self, account_update: ModelAccount, owner_member_id: str
    ) -> ModelAccount:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, account_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelAccount(
                    id=new_id,
                    child_id=account_update.id,
                    reference_id=account_update.reference_id,
                    name=account_update.name,
                    email=account_update.email,
                    description=account_update.description,
                    website=account_update.website,
                    member=account_update.member,
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
            LOGGER.logger.error(f"Unexpected error when creating account: {exc}")
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(f"Unexpected error when update account: {str(exc)}")
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelAccount)
                .where(
                    and_(
                        ModelAccount.reference_id == id,
                        ModelAccount.deleted_by.is_(None),
                        ModelAccount.deleted_at.is_(None),
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
            LOGGER.logger.error(f"Unexpected error when delete a account: {str(exc)}")
            raise exc
