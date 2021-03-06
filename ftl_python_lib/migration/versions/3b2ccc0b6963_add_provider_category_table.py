"""add provider category table

Revision ID: 3b2ccc0b6963
Revises: 91adb40f06b9
Create Date: 2022-05-27 12:53:53.686115

"""
import sqlalchemy as sa
from alembic import op

from ftl_python_lib.models.sql.member import ModelMember
from ftl_python_lib.models.sql.provider_category import ModelProviderCategory

# revision identifiers, used by Alembic.
revision = "3b2ccc0b6963"
down_revision = "91adb40f06b9"
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
    f"DROP TRIGGER IF EXISTS after_{ModelProviderCategory.__tablename__}_insert;"
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        ModelProviderCategory.__tablename__,
        sa.Column("id", sa.CHAR(length=36), nullable=False, autoincrement=False),
        sa.Column("reference_id", sa.CHAR(length=36), nullable=True),
        sa.Column("child_id", sa.CHAR(length=36), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("description", sa.TEXT, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("created_by", sa.CHAR(length=36), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_by", sa.CHAR(length=36), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_foreign_key(
        ModelProviderCategory.__tablename__ + "_fk_created_by",
        ModelProviderCategory.__tablename__,
        ModelMember.__tablename__,
        ["created_by"],
        ["id"],
    )

    op.execute(
        create_trigger.replace("__tablename__", ModelProviderCategory.__tablename__)
    )

    op.bulk_insert(
        ModelProviderCategory.__table__,
        [
            {
                "id": "5d3bf644-12e7-41e6-ad78-85b8f2fb2005",
                "name": "Infrastructure",
                "code": "infra",
                "description": "Infrastructure is the collection of hardware and software elements needed to enable cloud computing.",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": "b39e4c33-70e7-4421-92e1-2a23ef79db12",
                "name": "Data",
                "code": "data",
                "description": "Databases and data services allowing to connect to each other by effortlessly sharing and consuming shared data.",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": "9a18069d-4312-4527-a4e2-b4dd98c46f92",
                "name": "Clients",
                "code": "client",
                "description": "Computer hardware and/or software that relies on cloud computing for application delivery (e.g. data producer or data consumer).",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
        ],
    )

    op.create_index("name", ModelProviderCategory.__tablename__, ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(drop_trigger)
    op.drop_constraint(
        ModelProviderCategory.__tablename__ + "_fk_created_by",
        ModelProviderCategory.__tablename__,
        type_="foreignkey",
    )
    op.drop_index("name", table_name=ModelProviderCategory.__tablename__)
    op.drop_table(ModelProviderCategory.__tablename__)
    # ### end Alembic commands ###
