"""Create records related to one another via SQLAlchemy's ORM."""

import uuid
from types import NoneType

from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy import update

from ftl_python_lib.constants.models.member import ConstantsMemberRole
from ftl_python_lib.core.context.environment import EnvironmentContext
from ftl_python_lib.core.context.request import RequestContext
from ftl_python_lib.core.context.session import SessionContext
from ftl_python_lib.core.log import LOGGER
from ftl_python_lib.core.providers.aws.cognito import ProviderCognito
from ftl_python_lib.models.sql.member import ModelMember


class HelperMember:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Member")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()
        self.__cognito = ProviderCognito(
            request_context=self.__request_context,
            environ_context=self.__environ_context,
        )

    def get_by_auth_id(self, id: str, auth_email: str) -> ModelMember:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            member: ModelMember = (
                self.__session.query(ModelMember)
                .filter(
                    and_(
                        ModelMember.auth_id == id,
                        ModelMember.deleted_by.is_(None),
                        ModelMember.deleted_at.is_(None),
                    )
                )
                .first()
            )

            if member is None:
                response = self.create(
                    member_new=ModelMember(auth_id=id, email=auth_email),
                    owner_member_id=id,
                )

                return response

            return member
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get member by id: {str(exc)}")
            raise exc

    def get_by_id(self, id: str) -> ModelMember:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMember)
                .filter(
                    and_(
                        ModelMember.id == id,
                        ModelMember.deleted_by.is_(None),
                        ModelMember.deleted_at.is_(None),
                    )
                )
                .first()
            )
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get member by id: {str(exc)}")
            raise exc

    def get_reference_id(self, id: str) -> ModelMember:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMember)
                .filter(
                    and_(
                        ModelMember.reference_id == id,
                        ModelMember.deleted_by.is_(None),
                        ModelMember.deleted_at.is_(None),
                    )
                )
                .first()
            )
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get member by reference_id: {str(exc)}"
            )
            raise exc

    def get_all(self):
        """
        Retrive all records.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelMember)
                .filter(
                    and_(
                        ModelMember.deleted_by.is_(None),
                        ModelMember.deleted_at.is_(None),
                    )
                )
                .all()
            )
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get all members: {str(exc)}")
            raise exc

    def update(self, member_update: ModelMember, owner_member_id: str) -> ModelMember:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, member_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self.__session.add(
                ModelMember(
                    id=new_id,
                    child_id=member_update.id,
                    reference_id=member_update.reference_id,
                    auth_id=member_update.auth_id,
                    email=member_update.email,
                    first_name=member_update.first_name,
                    last_name=member_update.last_name,
                    avatar=member_update.avatar,
                    role=member_update.role,
                    invite=member_update.invite,
                    created_by=owner_member_id,
                )
            )
            self.__session.commit()

            return self.get_by_id(new_id)
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(f"Unexpected error when update member: {str(exc)}")
            raise exc

    def create(self, member_new: ModelMember, owner_member_id: str) -> ModelMember:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param member: New member record to create.
        :type member: ModelMember

        :return: Optional[ModelMember]
        """

        try:
            new_id = str(uuid.uuid4())
            member_new.id = new_id
            if member_new.role is None:
                member_new.role = ConstantsMemberRole.VIEWER.value
            member_new.created_by = owner_member_id

            self.__session.add(member_new)
            self.__session.commit()

            member = self.get_by_id(new_id)

            return member
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get member by id: {str(exc)}")
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Delete record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelMember)
                .where(
                    and_(
                        ModelMember.reference_id == id,
                        ModelMember.deleted_by.is_(None),
                        ModelMember.deleted_at.is_(None),
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
            LOGGER.logger.error(f"Unexpected error when delete a member: {str(exc)}")
            raise exc

    def invite(self, new_member):
        response = self.__cognito.invite(new_member["email"])
        if response["code"] == 201:
            self.create(
                member_new=ModelMember(
                    auth_id=response["data"]["User"]["Username"],
                    email=new_member["email"],
                    first_name=new_member["first_name"],
                    last_name=new_member["last_name"],
                    role=new_member["role"],
                    invite=text("true"),
                ),
                owner_member_id=new_member["owner"],
            )
        return response
