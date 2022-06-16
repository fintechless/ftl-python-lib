"""add microservice table

Revision ID: a6b2026c6047
Revises: 8877fe352467
Create Date: 2022-04-26 13:45:03.356686

"""
import sqlalchemy as sa
from alembic import op

from ftl_python_lib.models.sql.member import ModelMember
from ftl_python_lib.models.sql.microservice import ModelMicroservice

# revision identifiers, used by Alembic.
revision = "a6b2026c6047"
down_revision = "8877fe352467"
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
drop_trigger = f"DROP TRIGGER IF EXISTS after_{ModelMicroservice.__tablename__}_insert;"


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        ModelMicroservice.__tablename__,
        sa.Column("id", sa.CHAR(length=36), nullable=False, autoincrement=False),
        sa.Column("reference_id", sa.CHAR(length=36), nullable=True),
        sa.Column("child_id", sa.CHAR(length=36), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column(
            "active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("path", sa.Text(), nullable=True),
        sa.Column("runtime", sa.String(length=100), nullable=True),
        sa.Column("code", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("created_by", sa.CHAR(length=36), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_by", sa.CHAR(length=36), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_foreign_key(
        ModelMicroservice.__tablename__ + "_fk_created_by",
        ModelMicroservice.__tablename__,
        ModelMember.__tablename__,
        ["created_by"],
        ["id"],
    )

    op.execute(create_trigger.replace("__tablename__", ModelMicroservice.__tablename__))

    op.bulk_insert(
        ModelMicroservice.__table__,
        [
            {
                "id": "b14a5198-be76-4519-be17-6e6fc9f3f475",
                "name": "Message In MSA",
                "active": "true",
                "description": "Incoming Messages MicroService: receives and validates ISO 20022 message, transforms into internal format and sends to corresponding processing workflow.",
                "path": "https://ftl-api-runtime-default-us-east-1-123456789012.s3.amazonaws.com/git/fintechless/ftl-msa-msg-in/main",
                "runtime": "python",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": "fc387ab0-6905-4f39-991e-090002345c9f",
                "name": "Message PACS 008 MSA",
                "active": "true",
                "description": "PACS 008 Messages MicroService: receives internal format incoming message, processes according pacs 008 specific workflow and sends internal format outgoing message.",
                "path": "https://ftl-api-runtime-default-us-east-1-123456789012.s3.amazonaws.com/git/fintechless/ftl-msa-msg-pacs-008/main",
                "runtime": "python",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": "c0eb4932-81de-48f2-a691-cdfa9533a947",
                "name": "Message Out MSA",
                "active": "true",
                "description": "Outgoing Messages MicroService: receives internal format message, transforms into ISO 20022 format and notifies appropriate client.",
                "path": "https://ftl-api-runtime-default-us-east-1-123456789012.s3.amazonaws.com/git/fintechless/ftl-msa-msg-out/main",
                "runtime": "python",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": "d20ea2c7-3f1b-4f31-ae6a-6c84eaa91f8c",
                "name": "RabbitMQ In MSA",
                "active": "false",
                "description": "Incoming RabbitMQ MicroService: pulls messages from RabbitMQ incoming queue and pushes them into Fintechless API.",
                "path": "https://ftl-api-runtime-default-us-east-1-123456789012.s3.amazonaws.com/git/fintechless/ftl-msa-rmq-in/main",
                "runtime": "python",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": "9efe2dd6-2e27-444d-9b1f-718f80c33292",
                "name": "RabbitMQ Out MSA",
                "active": "false",
                "description": "Outgoing RabbitMQ MicroService: pulls messages from Fintechless API and pushes them into RabbitMQ outgoing queue.",
                "path": "https://ftl-api-runtime-default-us-east-1-123456789012.s3.amazonaws.com/git/fintechless/ftl-msa-rmq-out/main",
                "runtime": "python",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
        ],
    )

    op.create_index("name", ModelMicroservice.__tablename__, ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(drop_trigger)
    op.drop_constraint(
        ModelMicroservice.__tablename__ + "_fk_created_by",
        ModelMicroservice.__tablename__,
        type_="foreignkey",
    )
    op.drop_index("name", table_name=ModelMicroservice.__tablename__)
    op.drop_table(ModelMicroservice.__tablename__)
    # ### end Alembic commands ###
