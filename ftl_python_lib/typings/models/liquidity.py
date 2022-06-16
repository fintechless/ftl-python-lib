"""
Liquidity type definitions
"""


class TypeLiquidity(dict):
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
    def request_id(self) -> str:
        """
        Get request_id value
        """

        return self.get("request_id")

    @property
    def requested_at(self) -> str:
        """
        Get requested_at value
        """

        return self.get("requested_at")

    @property
    def deployment_id(self) -> str:
        """
        Get deployment_id value
        """

        return self.get("deployment_id")

    @property
    def entity_id(self) -> str:
        """
        Get entity_id value
        """

        return self.get("entity_id")

    @property
    def user_id(self) -> str:
        """
        Get user_id value
        """

        return self.get("user_id")

    @property
    def currency(self) -> str:
        """
        Get currency value
        """

        return self.get("currency")

    @property
    def amount(self) -> int:
        """
        Get amount value
        """

        return int(self.get("amount"))

    @property
    def balance(self) -> int:
        """
        Get balance value
        """

        return int(self.get("balance"))
