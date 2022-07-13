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
                "response_code": "ACTC",
                "response_message": "ACTC",
                "description": "Payment initiated successfully",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "ACSP",
                "response_message": "ACSP",
                "description": "Payment processed successfully",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "ACSC",
                "response_message": "ACSC",
                "description": "Payment released successfully",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC02",
                "response_message": "RJCT",
                "description": "Debtor account number invalid or missing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC03",
                "response_message": "RJCT",
                "description": "Creditor account number invalid or missing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC04",
                "response_message": "RJCT",
                "description": "Account number specified has been closed on the bank of account's books",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC06",
                "response_message": "RJCT",
                "description": "Account specified is blocked, prohibiting posting of transactions against it",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC11",
                "response_message": "RJCT",
                "description": "Creditor account currency is invalid or missing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC13",
                "response_message": "RJCT",
                "description": "Debtor account type invalid",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AC14",
                "response_message": "RJCT",
                "description": "Creditor account type invalid",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AG01",
                "response_message": "RJCT",
                "description": "Transaction forbidden on this type of account (formerly NoAgreement)",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AG03",
                "response_message": "RJCT",
                "description": "Transaction type not supported / authorized on this account",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AGNT",
                "response_message": "RJCT",
                "description": "Incorrect Agent",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AM02",
                "response_message": "RJCT",
                "description": "Specific transaction/message amount is greater than allowed maximum",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AM04",
                "response_message": "RJCT",
                "description": "Amount of funds available to cover specified message amount is insufficient",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AM09",
                "response_message": "RJCT",
                "description": "Amount received is not the amount agreed or expected",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AM12",
                "response_message": "RJCT",
                "description": "Amount is invalid or missing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AM13",
                "response_message": "RJCT",
                "description": "Transaction amount exceeds limits set by clearing system",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "AM14",
                "response_message": "RJCT",
                "description": "Transaction amount exceeds limits agreed between bank and client",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "ARDT",
                "response_message": "RJCT",
                "description": "Cancellation not accepted as the transaction has already been returned",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "BE04",
                "response_message": "RJCT",
                "description": "Specification of creditor's address, which is required for payment, is missing/not correct (formerly IncorrectCreditorAddress)",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "BE06",
                "response_message": "RJCT",
                "description": "End customer specified is not known at associated Sort/National Bank Code or does no longer exist in the books",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "BE07",
                "response_message": "RJCT",
                "description": "Specification of debtor's address, which is required for payment, is missing/not correct",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "BE10",
                "response_message": "RJCT",
                "description": "Debtor country code is missing or invalid",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "BE11",
                "response_message": "RJCT",
                "description": "Creditor country code is missing or invalid",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "BE16",
                "response_message": "RJCT",
                "description": "Debtor identification code missing or invalid",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "BE17",
                "response_message": "RJCT",
                "description": "Creditor identification code missing or invalid",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "CH11",
                "response_message": "RJCT",
                "description": "Creditor Identifier Incorrect",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "CUST",
                "response_message": "RJCT",
                "description": "Reported when the cancellation cannot be accepted because of a customer decision",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "DS04",
                "response_message": "RJCT",
                "description": "Order Rejected",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "DS0H",
                "response_message": "RJCT",
                "description": "Signer is not allowed to sign for this account",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "DS24",
                "response_message": "RJCT",
                "description": "Waiting time expired due to incomplete order",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "DT04",
                "response_message": "RJCT",
                "description": "Future date not supported",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "DUPL",
                "response_message": "RJCT",
                "description": "Payment is a duplicate of another payment",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "FF02",
                "response_message": "RJCT",
                "description": "Syntax error reason is provided as narrative information in the additional reason information",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "FF08",
                "response_message": "RJCT",
                "description": "End to End Id missing or invalid",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "FRAD",
                "response_message": "RJCT",
                "description": "Debtor claims payment was unauthorized or fraudulently induced",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "FRTR",
                "response_message": "RJCT",
                "description": "Repeat attempt to prior non-response",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "LEGL",
                "response_message": "RJCT",
                "description": "Reported when the cancellation cannot be accepted because of regulatory rules",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "MD07",
                "response_message": "RJCT",
                "description": "End customer is deceased",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "NARR",
                "response_message": "RJCT",
                "description": "Reason is provided as narrative information in the additional reason information",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "NOAS",
                "response_message": "RJCT",
                "description": "No response from beneficiary (to the cancellation request)",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "NOOR",
                "response_message": "RJCT",
                "description": "Original transaction (subject to cancellation) never received",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "RC01",
                "response_message": "RJCT",
                "description": "Bank identifier code specified in the message has an incorrect format (formerly IncorrectFormatForRoutingCode)",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "RC02",
                "response_message": "RJCT",
                "description": "Bank identifier is invalid or missing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "RC03",
                "response_message": "RJCT",
                "description": "Debtor FI identifier is invalid or missing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "RC04",
                "response_message": "RJCT",
                "description": "Creditor FI identifier is invalid or missing",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "SL03",
                "response_message": "RJCT",
                "description": "Token Service did not respond",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TECH",
                "response_message": "RJCT",
                "description": "Cancellation requested following technical problems resulting in an erroneous transaction",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TK01",
                "response_message": "RJCT",
                "description": "Invalid Token",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TK02",
                "response_message": "RJCT",
                "description": "Sender Token Not Found",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TK03",
                "response_message": "RJCT",
                "description": "Receiver Token Not Found",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TK04",
                "response_message": "RJCT",
                "description": "Token Expired",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TK05",
                "response_message": "RJCT",
                "description": "Token Found with Counterparty Mismatch",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TK06",
                "response_message": "RJCT",
                "description": "Token Found with Value Limit Rule Violation",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TK07",
                "response_message": "RJCT",
                "description": "Single Use Token Already Used",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TK08",
                "response_message": "RJCT",
                "description": "Token Suspended",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "TM01",
                "response_message": "RJCT",
                "description": "Invalid Cut Off Time",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            },
            {
                "id": str(uuid.uuid4()),
                "response_code": "UPAY",
                "response_message": "RJCT",
                "description": "Payment has been made through another payment channel (for Request for Payment expiry)",
                "created_by": "cb308772-c49d-11ec-9d64-0242ac120002"
            }
        ],
    )


def downgrade():
    pass
