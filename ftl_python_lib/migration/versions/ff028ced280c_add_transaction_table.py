"""add transaction table

Revision ID: ff028ced280c
Revises: 0608a8b318ec
Create Date: 2022-05-05 13:05:52.482926

"""
import uuid

import sqlalchemy as sa
from alembic import op

from ftl_python_lib.models.sql.member import ModelMember
from ftl_python_lib.models.sql.transaction import ModelTransaction
from ftl_python_lib.models.sql.transaction_type import ModelTransactionType

# revision identifiers, used by Alembic.
revision = "ff028ced280c"
down_revision = "0608a8b318ec"
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
drop_trigger = f"DROP TRIGGER IF EXISTS after_{ModelTransaction.__tablename__}_insert;"


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        ModelTransaction.__tablename__,
        sa.Column("id", sa.CHAR(length=36), nullable=False, autoincrement=False),
        sa.Column("reference_id", sa.CHAR(length=36), nullable=True),
        sa.Column("child_id", sa.CHAR(length=36), nullable=True),
        sa.Column("type_id", sa.CHAR(length=36), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False
        ),
        sa.Column("microservices", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("created_by", sa.CHAR(length=36), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_by", sa.CHAR(length=36), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_foreign_key(
        ModelTransaction.__tablename__ + "_fk_created_by",
        ModelTransaction.__tablename__,
        ModelMember.__tablename__,
        ["created_by"],
        ["id"],
    )

    op.create_foreign_key(
        ModelTransaction.__tablename__ + "_fk_type_id",
        ModelTransaction.__tablename__,
        ModelTransactionType.__tablename__,
        ["type_id"],
        ["id"],
    )

    op.execute(create_trigger.replace("__tablename__", ModelTransaction.__tablename__))

    op.bulk_insert(
        ModelTransaction.__table__,
        [
            {
                "id": str(uuid.uuid4()),
                "type_id": "c0297a2d-d0f4-49ec-89f5-7422bf465fdf",
                "name": "Payment Clearing",
                "description": "MicroServices driven workflow that accepts and processes Payments Clearing and Settlement (aka PACS) related messages.",
                "active": 1,
                "microservices": """[
                    "b14a5198-be76-4519-be17-6e6fc9f3f475",
                    "fc387ab0-6905-4f39-991e-090002345c9f",
                    "c0eb4932-81de-48f2-a691-cdfa9533a947"
                ]""",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "type_id": "c0297a2d-d0f4-49ec-89f5-7422bf465fdf",
                "name": "Payment Initiation",
                "description": "MicroServices driven workflow that accepts and processes Payments Initiation (aka PAIN) related messages.",
                "active": 0,
                "microservices": """[
                    "b14a5198-be76-4519-be17-6e6fc9f3f475",
                    "c0eb4932-81de-48f2-a691-cdfa9533a947"
                ]""",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "type_id": "c0297a2d-d0f4-49ec-89f5-7422bf465fdf",
                "name": "Payment Clearing (RabbitMQ)",
                "description": "MicroServices driven workflow that accepts and processes Payments Clearing and Settlement (aka PACS) related messages via RabbitMQ.",
                "active": 0,
                "microservices": """[
                    "d20ea2c7-3f1b-4f31-ae6a-6c84eaa91f8c",
                    "b14a5198-be76-4519-be17-6e6fc9f3f475",
                    "fc387ab0-6905-4f39-991e-090002345c9f",
                    "c0eb4932-81de-48f2-a691-cdfa9533a947",
                    "9efe2dd6-2e27-444d-9b1f-718f80c33292"
                ]""",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "type_id": "c0297a2d-d0f4-49ec-89f5-7422bf465fdf",
                "name": "Payment Initiation (RabbitMQ)",
                "description": "MicroServices driven workflow that accepts and processes Payments Initiation (aka PAIN) related messages via RabbitMQ.",
                "active": 0,
                "microservices": """[
                    "d20ea2c7-3f1b-4f31-ae6a-6c84eaa91f8c",
                    "b14a5198-be76-4519-be17-6e6fc9f3f475",
                    "c0eb4932-81de-48f2-a691-cdfa9533a947",
                    "9efe2dd6-2e27-444d-9b1f-718f80c33292"
                ]""",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
        ],
    )

    op.create_index("name", ModelTransaction.__tablename__, ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(drop_trigger)
    op.drop_constraint(
        ModelTransaction.__tablename__ + "_fk_created_by",
        ModelTransaction.__tablename__,
        type_="foreignkey",
    )
    op.drop_constraint(
        ModelTransaction.__tablename__ + "_fk_type_id",
        ModelTransaction.__tablename__,
        type_="foreignkey",
    )
    op.drop_index("name", table_name=ModelTransaction.__tablename__)
    op.drop_table(ModelTransaction.__tablename__)
    # ### end Alembic commands ###
