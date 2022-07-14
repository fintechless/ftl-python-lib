"""Create records related to one another via SQLAlchemy's ORM."""

from sqlalchemy import and_

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.context.session import SessionContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.core.providers.aws.codebuild import ProviderCodeBuild
from ftl_python_lib.models.sql.microservice import ModelMicroservice


class HelperCodeBuild:
    def __init__(
        self,
        request_context: RequestContext,
        environ_context: EnvironmentContext,
        id: str,
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Build")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

        self.__codebuild_docker_active: ProviderCodeBuild = ProviderCodeBuild(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
            cloud_region=self.__environ_context.active_region,
            codebuild_name=self.__environ_context.codebuild_project_docker,
        )

        self.__codebuild_docker_passive: ProviderCodeBuild = ProviderCodeBuild(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
            cloud_region=self.__environ_context.passive_region,
            codebuild_name=self.__environ_context.codebuild_project_docker,
        )

        self.__codebuild_api_active: ProviderCodeBuild = ProviderCodeBuild(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
            cloud_region=self.__environ_context.active_region,
            codebuild_name=self.__environ_context.codebuild_project_api,
        )

        self.__codebuild_api_passive: ProviderCodeBuild = ProviderCodeBuild(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
            cloud_region=self.__environ_context.passive_region,
            codebuild_name=self.__environ_context.codebuild_project_api,
        )

        microservice = (
            self.__session.query(ModelMicroservice)
            .filter(
                and_(
                    ModelMicroservice.reference_id == id,
                    ModelMicroservice.deleted_by.is_(None),
                    ModelMicroservice.deleted_at.is_(None),
                )
            )
            .first()
        )

        path_tree = microservice.path.split("/")
        del path_tree[:3]
        self.__microservice_storage_active = "/".join(
            ["s3:/", self.__environ_context.runtime_bucket] + path_tree
        )
        self.__microservice_storage_passive = (
            self.__microservice_storage_active.replace(
                self.__environ_context.active_region,
                self.__environ_context.passive_region,
            )
        )

    def build_active(self):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            LOGGER.logger.debug(
                f"Start Build in {self.__environ_context.active_region} region"
            )

            self.__codebuild_docker_active.start_build(
                [
                    {
                        "name": "CICD_REPOSITORY_STORAGE",
                        "value": self.__microservice_storage_active,
                        "type": "PLAINTEXT",
                    }
                ]
            )

        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get microservice by id: {str(exc)}"
            )
            raise exc

    def build_passive(self):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            LOGGER.logger.debug(
                f"Start Build in {self.__environ_context.passive_region} region"
            )

            self.__codebuild_docker_passive.start_build(
                [
                    {
                        "name": "CICD_REPOSITORY_STORAGE",
                        "value": self.__microservice_storage_passive,
                        "type": "PLAINTEXT",
                    }
                ]
            )

        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get microservice by id: {str(exc)}"
            )
            raise exc
