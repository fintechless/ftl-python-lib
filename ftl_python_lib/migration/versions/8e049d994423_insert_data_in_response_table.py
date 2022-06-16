"""insert data in response table

Revision ID: 8e049d994423
Revises: 7109d8874bcf
Create Date: 2022-06-14 00:04:37.377724

"""
import uuid

import sqlalchemy as sa
from alembic import op

from ftl_python_lib.models.sql.response import ModelResponse

# revision identifiers, used by Alembic.
revision = "8e049d994423"
down_revision = "7109d8874bcf"
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(
        ModelResponse.__table__,
        [
            {
                "id": str(uuid.uuid4()),
                "response_code": "HTTP200",
                "response_message": "OK",
                "description": "The request processed successfully",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "HTTP201",
                "response_message": "Created",
                "description": "The request succeeded, and a new resource was created as a result",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "HTTP202",
                "response_message": "Accepted",
                "description": "The request has been received, but not yet acted upon",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "STATUS1",
                "response_message": "INITIATED",
                "description": "New transaction was initiated",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "STATUS2",
                "response_message": "FAILED",
                "description": "Transaction processing failed",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "STATUS3",
                "response_message": "REJECTED",
                "description": "Transaction was rejected",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "STATUS4",
                "response_message": "RECEIVED",
                "description": "Transaction was received",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "STATUS5",
                "response_message": "PENDING",
                "description": "Transaction is pending for processing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "STATUS6",
                "response_message": "RELEASED",
                "description": "Transaction was released successfully",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "STATUS7",
                "response_message": "NOTIFIED",
                "description": "Transaction sender notified",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "STATUS8",
                "response_message": "CANCELED",
                "description": "Transaction was canceled",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "ACTC",
                "response_message": "ACTC",
                "description": "Payment initiated successfully",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "ACSP",
                "response_message": "ACSP",
                "description": "Payment processed successfully",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "ACSC",
                "response_message": "ACSC",
                "description": "Payment released successfully",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC02",
                "response_message": "RJCT",
                "description": "Debtor account number invalid or missing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC03",
                "response_message": "RJCT",
                "description": "Creditor account number invalid or missing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC04",
                "response_message": "RJCT",
                "description": "Account number specified has been closed on the bank of account's books",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002",
            },
        ],
    )


def downgrade():
    pass
