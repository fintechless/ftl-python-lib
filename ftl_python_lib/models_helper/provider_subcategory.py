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
from ftl_python_lib.models.sql.provider_subcategory import ModelProviderSubcategory
from ftl_python_lib.models_helper.provider import HelperProvider


class HelperProviderSubcategory:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for ProviderSubcategory")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_provider_subcategory_object(self, search_result):
        provider_subcategory = ModelProviderSubcategory(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            name=search_result.name,
            code=search_result.code,
            description=search_result.description,
            created_by=search_result.created_by,
        )

        return provider_subcategory

    def get_by_id(self, id: str) -> ModelProviderSubcategory:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelProviderSubcategory)
                .filter(
                    and_(
                        ModelProviderSubcategory.id == id,
                        ModelProviderSubcategory.deleted_by.is_(None),
                        ModelProviderSubcategory.deleted_at.is_(None),
                    )
                )
                .first()
            )

            provider_subcategory = self._clone_provider_subcategory_object(
                search_result
            )

            return provider_subcategory
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get provider_subcategory by id: {str(exc)}"
            )
            raise exc

    def get_by_name(self, name: str) -> ModelProviderSubcategory:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_provider_subcategory = (
                self.__session.query(ModelProviderSubcategory)
                .filter(
                    and_(
                        ModelProviderSubcategory.name == name,
                        ModelProviderSubcategory.deleted_by.is_(None),
                        ModelProviderSubcategory.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_provider_subcategory
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get provider_subcategory by name: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str) -> ModelProviderSubcategory:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelProviderSubcategory)
                .filter(
                    and_(
                        ModelProviderSubcategory.reference_id == id,
                        ModelProviderSubcategory.deleted_by.is_(None),
                        ModelProviderSubcategory.deleted_at.is_(None),
                    )
                )
                .first()
            )

            provider_subcategory = self._clone_provider_subcategory_object(
                search_result
            )

            return provider_subcategory
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get provider_subcategory by reference_id: {str(exc)}"
            )
            raise exc

    def get_all_by_category_id(self, category_id: str):
        """
        Retrive all records by category id.

        :return: Session
        """

        try:
            provider_helper = HelperProvider(
                request_context=self.__request_context,
                environ_context=self.__environ_context,
            )
            subcategory_ids = provider_helper.get_all_subcategory_ids_by_category_id(
                category_id
            )

            return (
                self.__session.query(ModelProviderSubcategory)
                .filter(
                    and_(
                        ModelProviderSubcategory.deleted_by.is_(None),
                        ModelProviderSubcategory.deleted_at.is_(None),
                        ModelProviderSubcategory.reference_id.in_(subcategory_ids),
                    )
                )
                .order_by(asc(ModelProviderSubcategory.name))
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all provider subcategory by category id: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelProviderSubcategory)
                .filter(
                    and_(
                        ModelProviderSubcategory.deleted_by.is_(None),
                        ModelProviderSubcategory.deleted_at.is_(None),
                    )
                )
                .order_by(asc(ModelProviderSubcategory.name))
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all provider_subcategory: {str(exc)}"
            )
            raise exc

    def update(
        self,
        provider_subcategory_update: ModelProviderSubcategory,
        owner_member_id: str,
    ) -> ModelProviderSubcategory:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, provider_subcategory_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelProviderSubcategory(
                    id=new_id,
                    child_id=provider_subcategory_update.id,
                    reference_id=provider_subcategory_update.reference_id,
                    name=provider_subcategory_update.name,
                    code=provider_subcategory_update.code,
                    description=provider_subcategory_update.description,
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
                f"Unexpected error when creating provider_subcategory: {exc}"
            )
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(
                f"Unexpected error when update provider_subcategory: {str(exc)}"
            )
            raise exc

    def create(
        self, provider_subcategory_new: ModelProviderSubcategory, owner_member_id: str
    ) -> ModelProviderSubcategory:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param provider_subcategory_new: New provider_subcategory record to create.
        :type provider_subcategory_new: ModelProviderSubcategory

        :return: Optional[ModelProviderSubcategory]
        """

        try:
            new_id = str(uuid.uuid4())
            provider_subcategory_new.id = new_id
            provider_subcategory_new.created_by = owner_member_id

            self.__session.add(provider_subcategory_new)
            self.__session.commit()

            member = self.get_by_id(new_id)

            return member
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(
                f"Unexpected error when creating provider_subcategory: {exc}"
            )
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelProviderSubcategory)
                .where(
                    and_(
                        ModelProviderSubcategory.reference_id == id,
                        ModelProviderSubcategory.deleted_by.is_(None),
                        ModelProviderSubcategory.deleted_at.is_(None),
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
                f"Unexpected error when delete a provider_subcategory: {str(exc)}"
            )
            raise exc
