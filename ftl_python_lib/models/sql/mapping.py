import uuid

from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func

from ftl_python_lib.utils.iterable_base import IterableBase


class ModelMapping(IterableBase):
    __tablename__ = "mapping"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(CHAR(length=36), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(CHAR(length=36), nullable=True)
    activated_at = Column(DateTime, server_default=func.now(), nullable=True)
    source = Column(String(length=255), nullable=False)
    source_type = Column(CHAR(length=36), nullable=False)
    content_type = Column(String(length=255), nullable=True)
    message_type = Column(String(length=255), nullable=True)
    target = Column(String(length=255), nullable=False)

    def __repr__(self):
        return (
            "{"
            + f'"id": "{self.id}",'
            + f'"child_id": "{self.child_id}",'
            + f'"reference_id": "{self.reference_id}",'
            + f'"source": "{self.source}",'
            + f'"source_type": "{self.source_type}",'
            + f'"content_type": "{self.content_type}",'
            + f'"message_type": "{self.message_type}",'
            + f'"target": "{self.target}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
