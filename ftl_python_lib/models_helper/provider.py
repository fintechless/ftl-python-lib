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
from ftl_python_lib.models.sql.provider import ModelProvider


class HelperProvider:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Provider")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_provider_object(self, search_result):
        provider = ModelProvider(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            active=search_result.active,
            activated_at=search_result.activated_at,
            name=search_result.name,
            description=search_result.description,
            category_id=search_result.category_id,
            subcategory_id=search_result.subcategory_id,
            secret_ref=search_result.secret_ref,
            created_by=search_result.created_by,
        )

        return provider

    def get_by_id(self, id: str) -> ModelProvider:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelProvider)
                .filter(
                    and_(
                        ModelProvider.id == id,
                        ModelProvider.deleted_by.is_(None),
                        ModelProvider.deleted_at.is_(None),
                    )
                )
                .first()
            )

            provider = self._clone_provider_object(search_result)

            return provider
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get provider by id: {str(exc)}")
            raise exc

    def get_by_name(self, name: str) -> ModelProvider:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_provider = (
                self.__session.query(ModelProvider)
                .filter(
                    and_(
                        ModelProvider.name == name,
                        ModelProvider.deleted_by.is_(None),
                        ModelProvider.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_provider
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get provider by name: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str) -> ModelProvider:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelProvider)
                .filter(
                    and_(
                        ModelProvider.reference_id == id,
                        ModelProvider.deleted_by.is_(None),
                        ModelProvider.deleted_at.is_(None),
                    )
                )
                .first()
            )

            provider = self._clone_provider_object(search_result)

            return provider
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get provider by reference_id: {str(exc)}"
            )
            raise exc

    def get_all_subcategory_ids_by_category_id(self, category_id: str):
        """
        Retrive all subcategory ids by category id.

        :return: list
        """

        try:
            subcategory_ids = []
            for item in (
                self.__session.query(ModelProvider)
                .filter(
                    and_(
                        ModelProvider.category_id == category_id,
                        ModelProvider.deleted_by.is_(None),
                        ModelProvider.deleted_at.is_(None),
                    )
                )
                .order_by(asc(ModelProvider.name))
                .all()
            ):
                subcategory_ids.append(item.subcategory_id)

            return subcategory_ids
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all subcategory ids by category id: {str(exc)}"
            )
            raise exc

    def get_all_by_category_id_subcategory_id(
        self, category_id: str, subcategory_id: str
    ):
        """
        Retrive all subcategory ids by category id.

        :return: list
        """

        try:
            return (
                self.__session.query(ModelProvider)
                .filter(
                    and_(
                        ModelProvider.category_id == category_id,
                        ModelProvider.subcategory_id == subcategory_id,
                        ModelProvider.deleted_by.is_(None),
                        ModelProvider.deleted_at.is_(None),
                    )
                )
                .order_by(asc(ModelProvider.name))
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all subcategory ids by category id: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelProvider)
                .filter(
                    and_(
                        ModelProvider.deleted_by.is_(None),
                        ModelProvider.deleted_at.is_(None),
                    )
                )
                .order_by(asc(ModelProvider.name))
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get all provider: {str(exc)}")
            raise exc

    def update(
        self, provider_update: ModelProvider, owner_member_id: str
    ) -> ModelProvider:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, provider_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelProvider(
                    id=new_id,
                    child_id=provider_update.id,
                    reference_id=provider_update.reference_id,
                    name=provider_update.name,
                    description=provider_update.description,
                    active=provider_update.active,
                    activated_at=provider_update.activated_at,
                    category_id=provider_update.category_id,
                    subcategory_id=provider_update.subcategory_id,
                    secret_ref=provider_update.secret_ref,
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
            LOGGER.logger.error(f"Unexpected error when creating provider: {exc}")
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(f"Unexpected error when update provider: {str(exc)}")
            raise exc

    def create(
        self, provider_new: ModelProvider, owner_member_id: str
    ) -> ModelProvider:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param provider_new: New provider record to create.
        :type provider_new: ModelProvider

        :return: Optional[ModelProvider]
        """

        try:
            new_id = str(uuid.uuid4())
            provider_new.id = new_id
            provider_new.created_by = owner_member_id

            self.__session.add(provider_new)
            self.__session.commit()

            member = self.get_by_id(new_id)

            return member
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(f"Unexpected error when creating provider: {exc}")
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelProvider)
                .where(
                    and_(
                        ModelProvider.reference_id == id,
                        ModelProvider.deleted_by.is_(None),
                        ModelProvider.deleted_at.is_(None),
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
            LOGGER.logger.error(f"Unexpected error when delete a provider: {str(exc)}")
            raise exc
