"""
Provider for AWS CodeBuild
"""

import boto3

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.decorators.exponential_backoff import DecoratorExponentialBackoff


# pylint: disable=R0903
class ProviderCodeBuild:
    """
    Provider for AWS CodeBuild
    """

    def __init__(
        self,
        request_context: RequestContext,
        environ_context: EnvironmentContext,
        cloud_region: str,
        codebuild_name: str,
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating CodeBuild provider")

        self.__request_context = request_context
        self.__environ_context = environ_context

        self.__codebuild_name: str = codebuild_name
        self.__codebuild_resource = boto3.client("codebuild", region_name=cloud_region)

    @DecoratorExponentialBackoff.retry(Exception)
    def start_build(self, environmentVariablesOverride):
        response = self.__codebuild_resource.start_build(
            projectName=self.__codebuild_name,
            environmentVariablesOverride=environmentVariablesOverride,
        )

        return response
