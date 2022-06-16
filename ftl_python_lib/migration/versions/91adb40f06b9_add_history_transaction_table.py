"""add history transaction table

Revision ID: 91adb40f06b9
Revises: 1bf893f2be27
Create Date: 2022-05-26 10:50:17.853295

"""
import sqlalchemy as sa
from alembic import op

from ftl_python_lib.models.sql.history_transaction import ModelHistoryTransaction
from ftl_python_lib.models.sql.member import ModelMember

# revision identifiers, used by Alembic.
revision = "91adb40f06b9"
down_revision = "1bf893f2be27"
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
drop_trigger = (
    f"DROP TRIGGER IF EXISTS after_{ModelHistoryTransaction.__tablename__}_insert;"
)


def upgrade():
    op.create_table(
        ModelHistoryTransaction.__tablename__,
        sa.Column("id", sa.CHAR(length=36), nullable=False),
        sa.Column("reference_id", sa.CHAR(length=36), nullable=True),
        sa.Column("child_id", sa.CHAR(length=36), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("created_by", sa.CHAR(length=36), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_by", sa.CHAR(length=36), nullable=True),
        sa.Column("request_id", sa.CHAR(length=36), nullable=False),
        sa.Column("requested_at", sa.DateTime, nullable=False),
        sa.Column("transaction_id", sa.CHAR(length=36), nullable=False),
        sa.Column("status", sa.String(length=255), nullable=False),
        sa.Column("message_type", sa.String(length=255), nullable=True),
        sa.Column("response_code", sa.String(length=255), nullable=True),
        sa.Column("response_message", sa.String(length=255), nullable=True),
        sa.Column("currency", sa.String(length=255), nullable=True),
        sa.Column("amount", sa.Float, nullable=True),
        sa.Column("retrieved_at", sa.DateTime, nullable=True),
        sa.Column("storage_path", sa.Text, nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_foreign_key(
        ModelHistoryTransaction.__tablename__ + "_fk_created_by",
        ModelHistoryTransaction.__tablename__,
        ModelMember.__tablename__,
        ["created_by"],
        ["id"],
    )

    op.execute(
        create_trigger.replace("__tablename__", ModelHistoryTransaction.__tablename__)
    )


def downgrade():
    op.execute(drop_trigger)

    op.drop_constraint(
        ModelHistoryTransaction.__tablename__ + "_fk_created_by",
        ModelHistoryTransaction.__tablename__,
        type_="foreignkey",
    )

    op.drop_table(ModelHistoryTransaction.__tablename__)
