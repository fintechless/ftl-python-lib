"""add response table

Revision ID: 1bf893f2be27
Revises: f2b4e935527d
Create Date: 2022-05-26 10:50:13.978125

"""
import sqlalchemy as sa
from alembic import op

from ftl_python_lib.models.sql.member import ModelMember
from ftl_python_lib.models.sql.response import ModelResponse

# revision identifiers, used by Alembic.
revision = "1bf893f2be27"
down_revision = "f2b4e935527d"
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
drop_trigger = f"DROP TRIGGER IF EXISTS after_{ModelResponse.__tablename__}_insert;"


def upgrade():
    op.create_table(
        ModelResponse.__tablename__,
        sa.Column("id", sa.CHAR(length=36), nullable=False),
        sa.Column("reference_id", sa.CHAR(length=36), nullable=True),
        sa.Column("child_id", sa.CHAR(length=36), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("created_by", sa.CHAR(length=36), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_by", sa.CHAR(length=36), nullable=True),
        sa.Column("response_code", sa.CHAR(length=255), nullable=False),
        sa.Column("response_message", sa.CHAR(length=255), nullable=False),
        sa.Column("description", sa.CHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_foreign_key(
        ModelResponse.__tablename__ + "_fk_created_by",
        ModelResponse.__tablename__,
        ModelMember.__tablename__,
        ["created_by"],
        ["id"],
    )

    op.execute(create_trigger.replace("__tablename__", ModelResponse.__tablename__))


def downgrade():
    op.execute(drop_trigger)

    op.drop_constraint(
        ModelResponse.__tablename__ + "_fk_created_by",
        ModelResponse.__tablename__,
        type_="foreignkey",
    )

    op.drop_table(ModelResponse.__tablename__)
