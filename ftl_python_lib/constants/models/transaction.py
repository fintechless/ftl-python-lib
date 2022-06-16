"""
Constants for Transaction
"""

from enum import Enum


class ConstantsTransactionStatus(Enum):
    """
    Transaction dictionary class - inherits the Enum class
    """

    INITIATED = "INITIATED"
    RECEIVED = "RECEIVED"
    REJECTED = "REJECTED"
    RETRIEVED = "RETRIEVED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    RELEASED = "RELEASED"
    NOTIFIED = "NOTIFIED"
