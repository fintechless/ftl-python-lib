"""Create records related to one another via SQLAlchemy's ORM."""

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.context.session import SessionContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.models.sql.mapping import ModelMapping


class HelperMapping:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Mapping")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

    def _clone_mapping_object(self, search_result):
        if search_result is None:
            return []

        mapping = []
        for it in search_result:
            mapping.append(
                ModelMapping(
                    id=it.id,
                    child_id=it.id,
                    reference_id=it.reference_id,
                    activated_at=it.activated_at,
                    source_type=it.source_type,
                    source=it.source,
                    target=it.target,
                    content_type=it.content_type,
                    message_type=it.message_type,
                    created_by=it.created_by,
                )
            )

        return mapping

    def get_all(
        self,
        source: str,
        source_type: str,
        content_type: str = None,
        message_type: str = None,
    ) -> ModelMapping:
        """
        Retrive record by source.

        :return: Session
        """

        filters = (
            (ModelMapping.source == source)
            & (ModelMapping.source_type == source_type)
            & (ModelMapping.deleted_by.is_(None))
            & (ModelMapping.deleted_at.is_(None))
        )

        if content_type is not None:
            filters = (
                (ModelMapping.source == source)
                & (ModelMapping.source_type == source_type)
                & (ModelMapping.content_type == content_type)
                & (ModelMapping.deleted_by.is_(None))
                & (ModelMapping.deleted_at.is_(None))
            )
        if message_type is not None:
            filters = (
                (ModelMapping.source == source)
                & (ModelMapping.source_type == source_type)
                & (ModelMapping.message_type == message_type)
                & (ModelMapping.deleted_by.is_(None))
                & (ModelMapping.deleted_at.is_(None))
            )
        if message_type is not None and content_type is not None:
            filters = (
                (ModelMapping.source == source)
                & (ModelMapping.source_type == source_type)
                & (ModelMapping.content_type == content_type)
                & (ModelMapping.message_type == message_type)
                & (ModelMapping.deleted_by.is_(None))
                & (ModelMapping.deleted_at.is_(None))
            )

        try:
            search_result = self.__session.query(ModelMapping).filter(filters).all()

            mapping = self._clone_mapping_object(search_result)

            return mapping
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get mapping by target: {str(exc)}"
            )
            raise exc
