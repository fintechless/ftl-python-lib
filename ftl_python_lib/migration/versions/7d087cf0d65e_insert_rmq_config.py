"""insert_rmq_config

Revision ID: 7d087cf0d65e
Revises: 4be503b72296
Create Date: 2022-07-06 23:55:28.117621

"""
import uuid

import sqlalchemy as sa
from alembic import op

from ftl_python_lib.models.sql.config import ModelConfig

# revision identifiers, used by Alembic.
revision = '7d087cf0d65e'
down_revision = '4be503b72296'
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(
        ModelConfig.__table__,
        [
            {
                "id": str(uuid.uuid4()),
                "var_key": "RABBITMQ_ENDPOINT",
                "active": True,
                "ref_table": "ftl-mgr-provider",
                "ref_key": "3d6d4953-c72b-4a73-8513-eaa3b17321e2",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "var_key": "RABBITMQ_PORT",
                "active": True,
                "ref_table": "ftl-mgr-provider",
                "ref_key": "3d6d4953-c72b-4a73-8513-eaa3b17321e2",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "var_key": "RABBITMQ_USERNAME",
                "active": True,
                "ref_table": "ftl-mgr-provider",
                "ref_key": "3d6d4953-c72b-4a73-8513-eaa3b17321e2",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "var_key": "RABBITMQ_PASSWORD",
                "active": True,
                "ref_table": "ftl-mgr-provider",
                "ref_key": "3d6d4953-c72b-4a73-8513-eaa3b17321e2",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
        ],
    )


def downgrade():
    pass
