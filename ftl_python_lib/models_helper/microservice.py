"""Create records related to one another via SQLAlchemy's ORM."""

import json
import uuid

from boto3 import client
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.exc import SQLAlchemyError

from ftl_python_lib.constants.models.microservice import ConstantsMicroserviceDefault
from ftl_python_lib.constants.models.microservice import ConstantsMicroserviceMapping
from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.context.session import SessionContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.core.providers.aws.s3 import ProviderS3
from ftl_python_lib.models.sql.microservice import ModelMicroservice
from ftl_python_lib.models.sql.transaction import ModelTransaction
from ftl_python_lib.typings.providers.aws.s3object import TypeS3Object


class HelperMicroservice:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Microservice")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()
        self.__provider_s3: ProviderS3 = ProviderS3(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )

    def get_by_id(self, id: str) -> ModelMicroservice:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMicroservice)
                .filter(
                    and_(
                        ModelMicroservice.id == id,
                        ModelMicroservice.deleted_by.is_(None),
                        ModelMicroservice.deleted_at.is_(None),
                    )
                )
                .first()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get microservice by id: {str(exc)}"
            )
            raise exc

    def get_by_reference_id(self, id: str) -> ModelMicroservice:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            return (
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
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get microservice by id: {str(exc)}"
            )
            raise exc

    def get_by_microservice_id(self, id: str) -> int:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelTransaction)
                .filter(
                    and_(
                        ModelTransaction.microservices.like('%"' + id + '"%'),
                        ModelTransaction.deleted_by.is_(None),
                        ModelTransaction.deleted_at.is_(None),
                    )
                )
                .scalar()
                or 0
            )

            return search_result
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get transaction by id: {str(exc)}"
            )
            raise exc

    def get_by_name(self, name: str) -> ModelMicroservice:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            existing_microservice = (
                self.__session.query(ModelMicroservice)
                .filter(
                    and_(
                        ModelMicroservice.name == name,
                        ModelMicroservice.deleted_by.is_(None),
                        ModelMicroservice.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_microservice
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get microservice by name: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMicroservice)
                .filter(
                    and_(
                        ModelMicroservice.deleted_by.is_(None),
                        ModelMicroservice.deleted_at.is_(None),
                    )
                )
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get all microservice: {str(exc)}"
            )
            raise exc

    def count(self):
        """
        Retrive count of all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMicroservice)
                .filter(
                    and_(
                        ModelMicroservice.deleted_by.is_(None),
                        ModelMicroservice.deleted_at.is_(None),
                    )
                )
                .count()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get count all microservice: {str(exc)}"
            )
            raise exc

    def count_active(self):
        """
        Retrive count of all active records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMicroservice)
                .filter(
                    and_(
                        ModelMicroservice.active.is_(True),
                        ModelMicroservice.deleted_by.is_(None),
                        ModelMicroservice.deleted_at.is_(None),
                    )
                )
                .count()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get count all active microservice: {str(exc)}"
            )
            raise exc

    def update(
        self,
        microservice_update: ModelMicroservice,
        owner_member_id: str,
        content: bytes,
        file_path: str,
    ) -> ModelMicroservice:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, microservice_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelMicroservice(
                    id=new_id,
                    child_id=microservice_update.id,
                    reference_id=microservice_update.reference_id,
                    name=microservice_update.name,
                    active=text(microservice_update.active),
                    description=microservice_update.description,
                    path=microservice_update.path,
                    runtime=microservice_update.runtime,
                    code=self._get_new_tree(microservice_update.path),
                    created_by=owner_member_id,
                )
            )

            if content is not None and file_path is not None:
                self.__provider_s3.put_object(
                    object=TypeS3Object(
                        bucket=self.__environ_context.runtime_bucket,
                        key=file_path,
                        body=content,
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
            LOGGER.logger.error(f"Unexpected error when creating microservice: {exc}")
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(
                f"Unexpected error when update microservice: {str(exc)}"
            )
            raise exc

    def _get_new_tree(self, path: str):
        code = None
        if path is not None:
            LOGGER.logger.debug(path)
            # will be fixed after making s3 private
            path_split = path.split(".s3.amazonaws.com/")
            bucket_name = path_split[0].replace("https://", "")
            prefix = path_split[1]
            s3_conn = client("s3")
            s3_result = s3_conn.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

            accumulator = []
            for key in s3_result["Contents"]:
                key_list = key["Key"].replace(prefix + "/", "").split("/")
                types = []
                for item in ConstantsMicroserviceMapping:
                    for item_value in item.value:
                        if item_value in key_list[0]:
                            type_name = str(item).replace(
                                "ConstantsMicroserviceMapping.", ""
                            )
                            if type_name not in types:
                                types.append(type_name)

                self.construct_dict(key_list, accumulator, types)
                code = json.dumps(accumulator)
        return code

    def construct_dict(self, in_list, accumulator, keys_name, parent=True):
        name = in_list[0]
        index = -1
        idx = -1
        for item in accumulator:
            idx = idx + 1
            if item["name"] == name:
                index = idx
                break
        if index < 0:
            if len(in_list[1::]) == 0:
                accumulator.append(
                    {
                        "name": name,
                        "type": keys_name,
                        "default": parent
                        and name in ConstantsMicroserviceDefault.DEFAULT.value,
                    }
                )
            else:
                accumulator.append(
                    {
                        "name": name,
                        "children": [],
                        "type": keys_name,
                        "default": parent
                        and name in ConstantsMicroserviceDefault.DEFAULT.value,
                    }
                )
            if len(in_list[1::]) != 0:
                self.construct_dict(
                    in_list[1::],
                    accumulator[len(accumulator) - 1]["children"],
                    keys_name,
                    False,
                )
        else:
            self.construct_dict(
                in_list[1::], accumulator[index]["children"], keys_name, False
            )

    def create(
        self, microservice_new: ModelMicroservice, owner_member_id: str
    ) -> ModelMicroservice:
        """
        Create a new microservice.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param microservice: New microservice record to create.
        :type microservice: ModelMicroservice

        :return: Optional[ModelMicroservice]
        """

        try:
            microservice_new.id = str(uuid.uuid4())
            microservice_new.code = self._get_new_tree(microservice_new.path)
            microservice_new.created_by = owner_member_id

            if microservice_new.active is not None:
                microservice_new.active = text(microservice_new.active)

            self.__session.add(microservice_new)
            self.__session.commit()

            return microservice_new
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(f"Unexpected error when creating microservice: {exc}")
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelMicroservice)
                .where(
                    and_(
                        ModelMicroservice.reference_id == id,
                        ModelMicroservice.deleted_by.is_(None),
                        ModelMicroservice.deleted_at.is_(None),
                    )
                )
                .values(
                    active=text("false"),
                    deleted_by=owner_member_id,
                    deleted_at=func.now(),
                )
                .execution_options(synchronize_session="fetch")
            )

            self.__session.execute(stmt)
            self.__session.commit()
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when delete a microservice: {str(exc)}"
            )
            raise exc
