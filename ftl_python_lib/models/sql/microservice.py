import uuid

from sqlalchemy import BOOLEAN
from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.sql import expression

from ftl_python_lib.utils.iterable_base import IterableBase


class ModelMicroservice(IterableBase):
    __tablename__ = "microservice"
    __identifier__ = "ftl-mgr-microservice"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    name = Column(String(length=100), nullable=False)
    child_id = Column(CHAR(length=36), nullable=True)
    active = Column(BOOLEAN, server_default=expression.true(), nullable=False)
    description = Column(Text, nullable=True)
    path = Column(Text, nullable=True)
    runtime = Column(String(length=100), nullable=True)
    code = Column(Text, nullable=True)
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
            + f'"active": "{self.active}",'
            + f'"description": "{self.description}",'
            + f'"path": "{self.path}",'
            + f'"runtime": "{self.runtime}",'
            + f'"code": "{self.code}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
