import uuid

from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func

from ftl_python_lib.utils.iterable_base import IterableBase


class ModelHistoryTransaction(IterableBase):
    __tablename__ = "history_transaction"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    created_by = Column(CHAR(length=36), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(CHAR(length=36), nullable=True)
    request_id = Column(CHAR(length=36), nullable=False)
    requested_at = Column(DateTime, nullable=False)
    transaction_id = Column(CHAR(length=36), nullable=False)
    status = Column(String(length=255), nullable=False)
    message_type = Column(String(length=255), nullable=True)
    response_code = Column(String(length=255), nullable=True)
    response_message = Column(String(length=255), nullable=True)
    currency = Column(String(length=255), nullable=True)
    amount = Column(Float, nullable=True)
    retrieved_at = Column(DateTime, nullable=True)
    storage_path = Column(Text, nullable=True)

    def __repr__(self):
        return (
            "{"
            + f'"id": "{self.id}",'
            + f'"child_id": "{self.child_id}",'
            + f'"reference_id": "{self.reference_id}",'
            + f'"request_id": "{self.request_id}",'
            + f'"requested_at": "{self.requested_at}",'
            + f'"transaction_id": "{self.transaction_id}",'
            + f'"status": "{self.status}"'
            + f'"message_type": "{self.message_type}"'
            + f'"response_code": "{self.response_code}"'
            + f'"response_message": "{self.response_message}"'
            + f'"currency": "{self.currency}"'
            + f'"amount": "{self.amount}"'
            + f'"retrieved_at": "{self.retrieved_at}"'
            + f'"storage_path": "{self.storage_path}"'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
