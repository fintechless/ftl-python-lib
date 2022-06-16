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


class ModelTransaction(IterableBase):
    __tablename__ = "transaction"
    __identifier__ = "ftl-mgr-transaction"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    type_id = Column(CHAR(length=36), nullable=False)
    name = Column(String(length=255), nullable=False)
    description = Column(TEXT, nullable=True)
    active = Column(BOOLEAN, server_default=expression.true(), nullable=False)
    microservices = Column(
        TEXT,
        server_default='["b14a5198-be76-4519-be17-6e6fc9f3f475"]',
        nullable=True,
    )
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
            + f'"type_id": "{self.type_id}",'
            + f'"name": "{self.name}",'
            + f'"description": "{self.description}",'
            + f'"active": "{self.active}",'
            + f'"microservices": "{self.microservices}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
