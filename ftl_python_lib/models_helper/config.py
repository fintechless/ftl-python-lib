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
from ftl_python_lib.core.providers.aws.secretsmanager import ProviderSecretsManager
from ftl_python_lib.models.sql.config import ModelConfig
from ftl_python_lib.models_helper.provider import HelperProvider


class HelperConfig:
    def __init__(
        self, request_context: RequestContext, environ_context: EnvironmentContext
    ) -> None:
        """
        Constructor
        """

        LOGGER.logger.debug("Creating model for Config")

        self.__request_context = request_context
        self.__environ_context = environ_context

        session = SessionContext()
        self.__session = session.get_session()

        self.__provider_secretsmanager: ProviderSecretsManager = ProviderSecretsManager(
            environ_context=self.__environ_context
        )
        self.__secretsmanager_values = {}

    def _clone_config_object(self, search_result):
        if hasattr(search_result, "ref_key") and search_result.ref_key is not None:
            helper_provider = HelperProvider(
                self.__request_context, self.__environ_context
            )
            provider = helper_provider.get_by_reference_id(search_result.ref_key)
            self.__secretsmanager_values = self.__provider_secretsmanager.get_value(
                provider.secret_ref
            )
        else:
            self.__secretsmanager_values = self.__provider_secretsmanager.get_value()

        var_value = ""
        if search_result.var_key in self.__secretsmanager_values:
            var_value = self.__secretsmanager_values[search_result.var_key]

        config = ModelConfig(
            id=search_result.id,
            child_id=search_result.id,
            reference_id=search_result.reference_id,
            active=search_result.active,
            activated_at=search_result.activated_at,
            var_key=search_result.var_key,
            var_value=var_value,
            ref_table=search_result.ref_table,
            ref_key=search_result.ref_key,
            created_by=search_result.created_by,
        )

        return config

    def get_by_id(self, id: str) -> ModelConfig:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelConfig)
                .filter(
                    and_(
                        ModelConfig.id == id,
                        ModelConfig.deleted_by.is_(None),
                        ModelConfig.deleted_at.is_(None),
                    )
                )
                .first()
            )

            config = self._clone_config_object(search_result)

            return config
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get config by id: {str(exc)}")
            raise exc

    def get_by_key(self, var_key: str, ref_table: str, ref_key: str) -> ModelConfig:
        """
        Retrive record by keys.

        :return: Session
        """

        try:
            existing_config = (
                self.__session.query(ModelConfig)
                .filter(
                    and_(
                        ModelConfig.var_key == var_key,
                        ModelConfig.ref_table == ref_table,
                        ModelConfig.ref_key == ref_key,
                        ModelConfig.deleted_by.is_(None),
                        ModelConfig.deleted_at.is_(None),
                    )
                )
                .first()
            )

            return existing_config
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get config by keys: {str(exc)}")
            raise exc

    def get_by_reference_id(self, id: str) -> ModelConfig:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            search_result = (
                self.__session.query(ModelConfig)
                .filter(
                    and_(
                        ModelConfig.reference_id == id,
                        ModelConfig.deleted_by.is_(None),
                        ModelConfig.deleted_at.is_(None),
                    )
                )
                .first()
            )

            config = self._clone_config_object(search_result)
            return config
        except Exception as exc:
            LOGGER.logger.error(
                f"Unexpected error when get config by reference_id: {str(exc)}"
            )
            raise exc

    def get_reference_id(self, id: str) -> ModelConfig:
        """
        Retrive record by id.

        :return: Session
        """

        try:
            return (
                self.__session.query(ModelConfig)
                .filter(
                    and_(
                        ModelConfig.reference_id == id,
                        ModelConfig.deleted_by.is_(None),
                        ModelConfig.deleted_at.is_(None),
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
            self.__secretsmanager_values = self.__provider_secretsmanager.get_value()
            return self._get_secretsmanager(
                (
                    self.__session.query(ModelConfig)
                    .filter(
                        and_(
                            ModelConfig.ref_table.is_(None),
                            ModelConfig.deleted_by.is_(None),
                            ModelConfig.deleted_at.is_(None),
                        )
                    )
                    .order_by(asc(ModelConfig.var_key))
                    .all()
                )
            )
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get all config: {str(exc)}")
            raise exc

    def get_all_by_identifier_id(
        self, identifier: str, identifier_id: str, secret_ref: str
    ):
        """
        Retrive all records.

        :return: Session
        """

        try:
            self.__secretsmanager_values = self.__provider_secretsmanager.get_value(
                secret_ref
            )
            return self._get_secretsmanager(
                (
                    self.__session.query(ModelConfig)
                    .filter(
                        and_(
                            ModelConfig.ref_table == identifier,
                            ModelConfig.ref_key == identifier_id,
                            ModelConfig.deleted_by.is_(None),
                            ModelConfig.deleted_at.is_(None),
                        )
                    )
                    .order_by(asc(ModelConfig.var_key))
                    .all()
                )
            )
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when get all config: {str(exc)}")
            raise exc

    def _get_secretsmanager(self, config_list):
        config_list_with_value = []
        for config in config_list:
            config_list_with_value.append(
                ModelConfig(
                    id=config.id,
                    reference_id=config.reference_id,
                    active=config.active,
                    activated_at=config.activated_at,
                    var_key=config.var_key,
                    var_value=self.__secretsmanager_values[config.var_key]
                    if config.var_key in self.__secretsmanager_values.keys()
                    else "N/A",
                )
            )

        return config_list_with_value

    def _set_secretsmanager(self, config, is_deleted: bool = False):
        if hasattr(config, "ref_key") and config.ref_key is not None:
            helper_provider = HelperProvider(
                self.__request_context, self.__environ_context
            )
            provider = helper_provider.get_by_reference_id(config.ref_key)
            self.__secretsmanager_values = self.__provider_secretsmanager.get_value(
                provider.secret_ref
            )
            self._set_or_unset(config, is_deleted)
            self.__secretsmanager_values = self.__provider_secretsmanager.put_value(
                self.__secretsmanager_values, provider.secret_ref
            )
        else:
            self.__secretsmanager_values = self.__provider_secretsmanager.get_value()
            self._set_or_unset(config, is_deleted)
            self.__secretsmanager_values = self.__provider_secretsmanager.put_value(
                self.__secretsmanager_values
            )

    def _set_or_unset(self, config, is_deleted):
        if is_deleted:
            if config.var_key in self.__secretsmanager_values:
                del self.__secretsmanager_values[config.var_key]
        else:
            self.__secretsmanager_values[config.var_key] = config.var_value

    def update(self, config_update: ModelConfig, owner_member_id: str) -> ModelConfig:
        """
        Update record.

        :return: Session
        """
        try:
            self.delete_by_id(owner_member_id, config_update.reference_id)
            new_id: str = str(uuid.uuid4())
            self._set_secretsmanager(config_update)
            self.__session.add(
                ModelConfig(
                    id=new_id,
                    child_id=config_update.id,
                    reference_id=config_update.reference_id,
                    active=config_update.active,
                    activated_at=config_update.activated_at,
                    var_key=config_update.var_key,
                    var_value=None,
                    ref_table=config_update.ref_table,
                    ref_key=config_update.ref_key,
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
            LOGGER.logger.error(f"Unexpected error when creating config: {exc}")
            raise exc
        except Exception as exc:
            self.__session.rollback()
            LOGGER.logger.error(f"Unexpected error when update config: {str(exc)}")
            raise exc

    def create(self, config_new: ModelConfig, owner_member_id: str) -> ModelConfig:
        """
        Create a new member.

        :param session: SQLAlchemy database session.
        :type session: Session
        :param config_new: New config record to create.
        :type config_new: ModelConfig

        :return: Optional[ModelConfig]
        """

        try:
            new_id = str(uuid.uuid4())
            config_new.id = new_id
            config_new.created_by = owner_member_id
            self._set_secretsmanager(config_new)
            config_new.var_value = None

            self.__session.add(config_new)
            self.__session.commit()
            member = self.get_by_id(new_id)

            return member
        except IntegrityError as exc:
            LOGGER.logger.error(exc)
            raise exc
        except SQLAlchemyError as exc:
            LOGGER.logger.error(f"Unexpected error when creating config: {exc}")
            raise exc

    def delete_by_id(self, owner_member_id: str, id: str):
        """
        Retrive record by id.

        :return: Session
        """

        try:
            stmt = (
                update(ModelConfig)
                .where(
                    and_(
                        ModelConfig.reference_id == id,
                        ModelConfig.deleted_by.is_(None),
                        ModelConfig.deleted_at.is_(None),
                    )
                )
                .values(
                    deleted_by=owner_member_id,
                    deleted_at=func.now(),
                )
                .execution_options(synchronize_session="fetch")
            )
            self._set_secretsmanager(self.get_by_reference_id(id), True)
            self.__session.execute(stmt)
            self.__session.commit()
        except Exception as exc:
            LOGGER.logger.error(f"Unexpected error when delete a config: {str(exc)}")
            raise exc
