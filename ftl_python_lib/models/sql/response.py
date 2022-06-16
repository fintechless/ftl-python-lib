import uuid

from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import func

from ftl_python_lib.utils.iterable_base import IterableBase


class ModelResponse(IterableBase):
    __tablename__ = "response"
    __identifier__ = "ftl-api-response"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(CHAR(length=36), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(CHAR(length=36), nullable=True)
    response_code = Column(String(length=255), nullable=True)
    response_message = Column(String(length=255), nullable=True)
    description = Column(String(length=255), nullable=True)

    def __repr__(self):
        return (
            "{"
            + f'"id": "{self.id}",'
            + f'"child_id": "{self.child_id}",'
            + f'"reference_id": "{self.reference_id}",'
            + f'"response_code": "{self.response_code}",'
            + f'"response_message": "{self.response_message}",'
            + f'"description": "{self.description}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
