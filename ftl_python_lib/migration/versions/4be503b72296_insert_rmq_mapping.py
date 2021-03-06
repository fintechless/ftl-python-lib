"""insert rmq mapping

Revision ID: 4be503b72296
Revises: 8e049d994423
Create Date: 2022-06-28 23:21:27.333058

"""
import uuid

from alembic import op

from ftl_python_lib.models.sql.mapping import ModelMapping

# revision identifiers, used by Alembic.
revision = "4be503b72296"
down_revision = "8e049d994423"
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(
        ModelMapping.__table__,
        [
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "queue-custom-msg-out-pacs-008",
                "source_type": "message_out",
                "content_type": "application/json",
                "message_type": "pacs.008",
                "target": "ftl-msa-rmq-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "queue-custom-msg-out-pacs-009",
                "source_type": "message_out",
                "content_type": "application/json",
                "message_type": "pacs.009",
                "target": "ftl-msa-rmq-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-out",
                "source_type": "message_out",
                "content_type": "application/json",
                "message_type": "pacs.008",
                "target": "ftl-msa-msg-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-out",
                "source_type": "message_out",
                "content_type": "application/json",
                "message_type": "pacs.009",
                "target": "ftl-msa-msg-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-out",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.008",
                "target": "ftl-msa-rmq-in",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-out",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.009",
                "target": "ftl-msa-rmq-in",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-in",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.009",
                "target": "queue-iso20022-msg-out-pacs-009",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-out",
                "source_type": "message_in",
                "content_type": "text/xml",
                "message_type": "pacs.002",
                "target": "ftl-msa-msg-in",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-out",
                "source_type": "message_in",
                "content_type": "text/xml",
                "message_type": "pacs.009",
                "target": "ftl-msa-msg-in",
            },
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
                "source": "ftl-msa-msg-pacs-009",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.009",
                "target": "ftl-msa-msg-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-out",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.002",
                "target": "ftl-msa-rmq-in",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-out",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.008",
                "target": "ftl-msa-rmq-in",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-out",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.009",
                "target": "ftl-msa-rmq-in",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-in",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.002",
                "target": "queue-iso20022-msg-out-pacs-002",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-in",
                "source_type": "message_out",
                "content_type": "text/xml",
                "message_type": "pacs.008",
                "target": "queue-iso20022-msg-out-pacs-008",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "queue-iso20022-msg-in-pacs-002",
                "source_type": "message_in",
                "content_type": "text/xml",
                "message_type": "pacs.002",
                "target": "ftl-msa-rmq-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "queue-iso20022-msg-in-pacs-008",
                "source_type": "message_in",
                "content_type": "text/xml",
                "message_type": "pacs.008",
                "target": "ftl-msa-rmq-out",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-out",
                "source_type": "message_in",
                "content_type": "text/xml",
                "message_type": "pacs.008",
                "target": "ftl-msa-msg-in",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-in",
                "source_type": "message_in",
                "content_type": "application/json",
                "message_type": "pacs.002",
                "target": "ftl-msa-rmq-in",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-msg-in",
                "source_type": "message_in",
                "content_type": "application/json",
                "message_type": "pacs.008",
                "target": "ftl-msa-rmq-in",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-in",
                "source_type": "message_in",
                "content_type": "application/json",
                "message_type": "pacs.002",
                "target": "queue-custom-msg-in-pacs-002",
            },
            {
                "id": str(uuid.uuid4()),
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
                "source": "ftl-msa-rmq-in",
                "source_type": "message_in",
                "content_type": "application/json",
                "message_type": "pacs.008",
                "target": "queue-custom-msg-in-pacs-008",
            },
        ],
    )


def downgrade():
    pass
