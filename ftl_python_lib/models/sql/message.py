import uuid

from sqlalchemy import BOOLEAN
from sqlalchemy import CHAR
from sqlalchemy import TEXT
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.sql import expression

from ftl_python_lib.utils.iterable_base import IterableBase


class ModelMessage(IterableBase):
    __tablename__ = "message"
    __identifier__ = "ftl-mgr-message"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    unique_key = Column(String(length=255), nullable=False)
    description = Column(TEXT, nullable=True)
    org = Column(String(length=255), nullable=True)
    url = Column(String(length=255), nullable=True)
    active = Column(BOOLEAN, server_default=expression.true(), nullable=False)
    storage_path = Column(TEXT, nullable=False)
    unique_type = Column(String(length=255), nullable=False)
    version_major = Column(String(length=255), nullable=False)
    version_minor = Column(String(length=255), nullable=False)
    version_patch = Column(String(length=255), nullable=False)
    category_id = Column(CHAR(length=36), nullable=True)
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
            + f'"unique_key": "{self.unique_key}",'
            + f'"description": "{self.description}",'
            + f'"org": "{self.org}",'
            + f'"url": "{self.url}",'
            + f'"storage_path": "{self.storage_path}",'
            + f'"unique_type": "{self.unique_type}",'
            + f'"version_major": "{self.version_major}",'
            + f'"version_minor": "{self.version_minor}",'
            + f'"version_patch": "{self.version_patch}",'
            + f'"active": "{self.active}",'
            + f'"category_id": "{self.category_id}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
