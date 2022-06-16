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


class ModelMember(IterableBase):
    __tablename__ = "member"
    __identifier__ = "ftl-api-member"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    auth_id = Column(CHAR(length=36), nullable=False)
    email = Column(String(length=255), nullable=True)
    first_name = Column(String(length=255), nullable=True)
    last_name = Column(String(length=255), nullable=True)
    avatar = Column(TEXT, nullable=True)
    role = Column(String(length=255), nullable=False)
    invite = Column(BOOLEAN, server_default=expression.true(), nullable=False)
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
            + f'"auth_id": "{self.auth_id}",'
            + f'"email": "{self.email}",'
            + f'"first_name": "{self.first_name}",'
            + f'"last_name": "{self.last_name}",'
            + f'"avatar": "{self.avatar}",'
            + f'"role": "{self.role}",'
            + f'"invite": "{self.invite}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
