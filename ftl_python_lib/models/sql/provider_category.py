import uuid

from sqlalchemy import CHAR
from sqlalchemy import TEXT
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func

from ftl_python_lib.utils.iterable_base import IterableBase


class ModelProviderCategory(IterableBase):
    __tablename__ = "provider_category"
    __identifier__ = "ftl-mgr-provider-category"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    name = Column(String(length=255), nullable=False)
    code = Column(String(length=255), nullable=False)
    description = Column(TEXT, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(CHAR(length=36), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(CHAR(length=36), nullable=True)

    def __repr__(self):
        return (
            "{"
            + f'"id": "{self.id}",'
            + f'"child_id": "{self.child_id}",'
            + f'"reference_id": "{self.reference_id}",'
            + f'"name": "{self.name}",'
            + f'"code": "{self.code}",'
            + f'"description": "{self.description}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
