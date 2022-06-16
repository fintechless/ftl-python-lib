"""add mapping table
Revision ID: f2b4e935527d
Revises: 9f53a732fc25
Create Date: 2022-05-18 17:09:20.815401
"""
import uuid

import sqlalchemy as sa
from alembic import op

from ftl_python_lib.models.sql.mapping import ModelMapping
from ftl_python_lib.models.sql.member import ModelMember

# revision identifiers, used by Alembic.
revision = "f2b4e935527d"
down_revision = "9f53a732fc25"
branch_labels = None
depends_on = None
create_trigger = """
    CREATE TRIGGER after___tablename___insert
    BEFORE INSERT
    ON __tablename__ FOR EACH ROW
    IF NEW.reference_id IS NULL THEN
        SET NEW.reference_id = NEW.id;
    END IF;
"""
drop_trigger = f"DROP TRIGGER IF EXISTS after_{ModelMapping.__tablename__}_insert;"


def upgrade():
    op.create_table(
        ModelMapping.__tablename__,
        sa.Column("id", sa.CHAR(length=36), nullable=False),
        sa.Column("reference_id", sa.CHAR(length=36), nullable=True),
        sa.Column("child_id", sa.CHAR(length=36), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("created_by", sa.CHAR(length=36), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_by", sa.CHAR(length=36), nullable=True),
        sa.Column(
            "activated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("source", sa.CHAR(length=255), nullable=False),
        sa.Column("source_type", sa.CHAR(length=36), nullable=False),
        sa.Column("content_type", sa.CHAR(length=255), nullable=True),
        sa.Column("message_type", sa.CHAR(length=255), nullable=True),
        sa.Column("target", sa.CHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_foreign_key(
        ModelMapping.__tablename__ + "_fk_created_by",
        ModelMapping.__tablename__,
        ModelMember.__tablename__,
        ["created_by"],
        ["id"],
    )
    op.execute(create_trigger.replace("__tablename__", ModelMapping.__tablename__))
    op.bulk_insert(
        ModelMapping.__table__,
        [
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-in",
                "source_type": "message_in",
                "content_type": "text/xml",
                "message_type": "pacs.002",
                "target": "ftl-msa-msg-pacs-002",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-in",
                "source_type": "message_in",
                "content_type": "text/xml",
                "message_type": "pacs.008",
                "target": "ftl-msa-msg-pacs-008",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-in",
                "source_type": "message_in",
                "content_type": "text/xml",
                "message_type": "pacs.009",
                "target": "ftl-msa-msg-pacs-009",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-in",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.002",
                "target": "ftl-msa-msg-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-pacs-002",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.002",
                "target": "ftl-msa-msg-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-pacs-008",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.008",
                "target": "ftl-msa-msg-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-pacs-008",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.002",
                "target": "ftl-msa-msg-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-pacs-009",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.009",
                "target": "ftl-msa-msg-out",
            },
        ],
    )


def downgrade():
    op.execute(drop_trigger)
    op.drop_constraint(
        ModelMapping.__tablename__ + "_fk_created_by",
        ModelMapping.__tablename__,
        type_="foreignkey",
    )
    op.drop_table(ModelMapping.__tablename__)
