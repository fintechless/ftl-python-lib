import uuid

from sqlalchemy import BOOLEAN
from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.sql import expression

from ftl_python_lib.utils.iterable_base import IterableBase


class ModelProvider(IterableBase):
    __tablename__ = "provider"
    __identifier__ = "ftl-mgr-provider"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(CHAR(length=36), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(CHAR(length=36), nullable=True)
    active = Column(BOOLEAN, server_default=expression.false(), nullable=False)
    activated_at = Column(DateTime, nullable=True)
    name = Column(String(length=255), nullable=False)
    description = Column(String(length=255), nullable=True)
    category_id = Column(CHAR(length=36), nullable=False)
    subcategory_id = Column(CHAR(length=36), nullable=False)
    secret_ref = Column(String(length=255), nullable=True)

    def __repr__(self):
        return (
            "{"
            + f'"id": "{self.id}",'
            + f'"child_id": "{self.child_id}",'
            + f'"reference_id": "{self.reference_id}",'
            + f'"active": "{self.active}",'
            + f'"activated_at": "{self.activated_at}",'
            + f'"name": "{self.name}",'
            + f'"description": "{self.description}",'
            + f'"category_id": "{self.category_id}",'
            + f'"subcategory_id": "{self.subcategory_id}",'
            + f'"secret_ref": "{self.secret_ref}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
