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
from ftl_python_lib.models.sql.provider_category import ModelProviderCategory


class HelperProviderCategory:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for ProviderCategory")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_provider_category_object(self, search_result):
        provider_category = ModelProviderCategory(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            name=search_result.name,
            code=search_result.code,
            description=search_result.description,
            created_by=search_result.created_by,
        )

        return provider_category

    def get_by_id(self, id: str) -> ModelProviderCategory:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelProviderCategory)
                .filter(
                    and_(
                        ModelProviderCategory.id == id,
                        ModelProviderCategory.deleted_by.is_(None),
                        ModelProviderCategory.deleted_at.is_(None),
                    )
                )
                .first()
            )

            provider_category = self._clone_provider_category_object(search_result)

            return provider_category
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get provider_category by id: {str(exc)}"
            )
            raise exc

    def get_by_name(self, name: str) -> ModelProviderCategory:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_provider_category = (
                self.__session.query(ModelProviderCategory)
                .filter(
                    and_(
                        ModelProviderCategory.name == name,
                        ModelProviderCategory.deleted_by.is_(None),
                        ModelProviderCategory.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_provider_category
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get provider_category by name: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str) -> ModelProviderCategory:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelProviderCategory)
                .filter(
                    and_(
                        ModelProviderCategory.reference_id == id,
                        ModelProviderCategory.deleted_by.is_(None),
                        ModelProviderCategory.deleted_at.is_(None),
                    )
                )
                .first()
            )

            provider_category = self._clone_provider_category_object(search_result)

            return provider_category
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get provider_category by reference_id: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelProviderCategory)
                .filter(
                    and_(
                        ModelProviderCategory.deleted_by.is_(None),
                        ModelProviderCategory.deleted_at.is_(None),
                    )
                )
                .order_by(asc(ModelProviderCategory.name))
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all provider_category: {str(exc)}"
            )
            raise exc

    def update(
        self, provider_category_update: ModelProviderCategory, owner_member_id: str
    ) -> ModelProviderCategory:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, provider_category_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelProviderCategory(
                    id=new_id,
                    child_id=provider_category_update.id,
                    reference_id=provider_category_update.reference_id,
                    name=provider_category_update.name,
                    code=provider_category_update.code,
                    description=provider_category_update.description,
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
                f"Unexpected error when creating provider_category: {exc}"
            )
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(
                f"Unexpected error when update provider_category: {str(exc)}"
            )
            raise exc

    def create(
        self, provider_category_new: ModelProviderCategory, owner_member_id: str
    ) -> ModelProviderCategory:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param provider_category_new: New provider_category record to create.
        :type provider_category_new: ModelProviderCategory

        :return: Optional[ModelProviderCategory]
        """

        try:
            new_id = str(uuid.uuid4())
            provider_category_new.id = new_id
            provider_category_new.created_by = owner_member_id

            self.__session.add(provider_category_new)
            self.__session.commit()

            member = self.get_by_id(new_id)

            return member
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(
                f"Unexpected error when creating provider_category: {exc}"
            )
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelProviderCategory)
                .where(
                    and_(
                        ModelProviderCategory.reference_id == id,
                        ModelProviderCategory.deleted_by.is_(None),
                        ModelProviderCategory.deleted_at.is_(None),
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
                f"Unexpected error when delete a provider_category: {str(exc)}"
            )
            raise exc
