"""
Provider for AWS S3
"""

import boto3
import botocore.exceptions
from mypy_boto3_s3 import S3ServiceResource
from mypy_boto3_s3.service_resource import Object
from mypy_boto3_s3.type_defs import PutObjectOutputTypeDef

from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.decorators.exponential_backoff import DecoratorExponentialBackoff
from ftl_python_lib.typings.providers.aws.s3object import TypeS3Object


# pylint: disable=R0903
class ProviderS3:
    """
    Provider for AWS S3
    :param __s3_resource: S3 boto3 resource
    :type __s3_resource: S3ServiceResource
    :param __bucket_name: Name of the s3 bucket
    :param __bucket_name: str
    :param __in_object_key: Incoming object key
    :param __in_object_key: str
    :param __out_object_key: Outgoing object key
    :param __out_object_key: str
    """

    __s3_resource: S3ServiceResource = boto3.resource("s3", region_name="us-east-1")

    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        :param bucket_name: Name of the S3 bucket
        :type bucket_name: str
        """

        LOGGER.logger.debug("Creating S3 provider")

        self.__request_context = request_context
        self.__environ_context = environ_context
        self.__s3_resource: S3ServiceResource = boto3.resource(
            "s3",
            region_name=self.__environ_context.active_region,
            endpoint_url=self.__environ_context.cloud_provider_api_endpoint_url,
        )
        self.__bucket_name: str = self.__environ_context.runtime_bucket

    @DecoratorExponentialBackoff.retry(Exception)
    def put_object(self, object: TypeS3Object) -> PutObjectOutputTypeDef:
        """
        Upload object to bucket
        :param object: Object
        :type object: TypeS3Object
        """

        LOGGER.logger.debug(
            f"Uploading object: key: {object.key}, bucket: {object.bucket}"
        )

        s3_object: Object = self.__s3_resource.Object(
            bucket_name=object.bucket, key=object.key
        )
        result = s3_object.put(Body=object.body)

        LOGGER.logger.debug(
            f"Object uploaded: key: {object.key}, bucket: {object.bucket}"
        )

        return result

    @DecoratorExponentialBackoff.retry(Exception)
    def get_object_body(self, key: str, bucket: str) -> bytes:
        """
        Get object body
        :param key: Object key
        :type key: str
        :param bucket: Bucket
        :type bucket: str
        """

        try:
            LOGGER.logger.debug(f"Retrieving object: key: {key}, bucket: {bucket}")

            s3_object: Object = self.__s3_resource.Object(bucket_name=bucket, key=key)

            result: bytes = s3_object.get().get("Body").read()

            LOGGER.logger.debug(f"Retrieved object: key: {key}, bucket: {bucket}")

            return result
        except botocore.exceptions.ClientError as exc:
            if exc.response.get("Error").get("Code") == "NoSuchKey":
                LOGGER.logger.error(
                    f"NoSuchKey! Could not retrieve object: key: {key}, bucket: {bucket}"
                )
                LOGGER.logger.error(
                    f"Returning empty body for object: key: {key}, bucket: {bucket}"
                )

                return b""

            raise exc
