import uuid

from sqlalchemy import BOOLEAN
from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.sql import expression

from ftl_python_lib.utils.iterable_base import IterableBase


class ModelConfig(IterableBase):
    __tablename__ = "config"
    __identifier__ = "ftl-api-config"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(CHAR(length=36), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(CHAR(length=36), nullable=True)
    active = Column(BOOLEAN, server_default=expression.false(), nullable=False)
    activated_at = Column(DateTime, nullable=True)
    var_key = Column(String(length=255), nullable=False)
    var_value = Column(String(length=255), nullable=True)
    ref_table = Column(CHAR(length=255), nullable=True)
    ref_key = Column(CHAR(length=36), nullable=True)

    def __repr__(self):
        return (
            "{"
            + f'"id": "{self.id}",'
            + f'"child_id": "{self.child_id}",'
            + f'"reference_id": "{self.reference_id}",'
            + f'"active": "{self.active}",'
            + f'"activated_at": "{self.activated_at}",'
            + f'"var_key": "{self.var_key}",'
            + f'"var_value": "{self.var_value}",'
            + f'"ref_table": "{self.ref_table}",'
            + f'"ref_key": "{self.ref_key}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
