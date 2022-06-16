"""
Transaction type definitions
"""


class TypeTransaction(dict):
    """
    Transaction custom type definition -- inherits dict type
    """

    @property
    def id(self) -> str:
        """
        Get id value
        """

        return self.get("id")

    @property
    def created_at(self) -> str:
        """
        Get created_at value
        """

        return self.get("created_at")

    @property
    def transaction_id(self) -> str:
        """
        Get transaction_id value
        """

        return self.get("transaction_id")

    @property
    def status(self) -> str:
        """
        Get status value
        """

        return self.get("status")

    @property
    def retrieved_at(self) -> str:
        """
        Get retrieved_at value
        """

        return self.get("retrieved_at")

    @retrieved_at.setter
    def retrieved_at(self, retrieved_at: str) -> None:
        """
        Set retrieved_at value
        :param retrieved_at: Was retrieved?
        :type retrieved_at: str
        """

        self.setdefault("retrieved_at", retrieved_at)
