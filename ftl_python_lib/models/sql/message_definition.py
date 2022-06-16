import uuid

from sqlalchemy import BOOLEAN
from sqlalchemy import CHAR
from sqlalchemy import SMALLINT
from sqlalchemy import TEXT
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.sql import expression

from ftl_python_lib.utils.iterable_base import IterableBase


class ModelMessageDefinition(IterableBase):
    __tablename__ = "message_definition"
    __identifier__ = "ftl-mgr-message-definition"
    id = Column(CHAR(length=36), primary_key=True, default=str(uuid.uuid4()))
    reference_id = Column(CHAR(length=36), nullable=True)
    child_id = Column(CHAR(length=36), nullable=True)
    name = Column(String(length=255), nullable=False)
    type = Column(TEXT, nullable=True)
    activated_at = Column(DateTime, nullable=True)
    message_id = Column(CHAR(length=36), nullable=False)
    xsd_tag = Column(TEXT, nullable=True)
    annotation_name = Column(String(length=255), nullable=True)
    annotation_definition = Column(TEXT, nullable=True)
    parent_id = Column(CHAR(length=36), nullable=True)
    level = Column(SMALLINT, nullable=True)
    is_leaf = Column(BOOLEAN, server_default=expression.true(), nullable=False)
    target_column = Column(String(length=255), nullable=True)
    target_type = Column(String(length=255), nullable=True)
    element_index = Column(Integer, nullable=True)
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
            + f'"type": "{self.type}",'
            + f'"activated_at": "{self.activated_at}",'
            + f'"message_id": "{self.message_id}",'
            + f'"xsd_tag": "{self.xsd_tag}",'
            + f'"annotation_name": "{self.annotation_name}",'
            + f'"annotation_definition": "{self.annotation_definition}",'
            + f'"parent_id": "{self.parent_id}",'
            + f'"level": "{self.level}",'
            + f'"is_leaf": "{self.is_leaf}",'
            + f'"target_column": "{self.target_column}",'
            + f'"target_type": "{self.target_type}",'
            + f'"created_by": "{self.created_by}"'
            + "}"
        )
