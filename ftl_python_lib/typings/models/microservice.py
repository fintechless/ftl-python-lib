"""
Microservice type definitions
"""


class TypeMicroservice(dict):
    """
    Microservice custom type definition -- inherits dict type
    """

    @property
    def id(self) -> str:
        """
        Get id value
        """

        return self.get("id")

    @property
    def reference_id(self) -> str:
        """
        Get reference_id value
        """

        return self.get("reference_id")

    @property
    def name(self) -> str:
        """
        Get name value
        """

        return self.get("name")

    @property
    def child_id(self) -> str:
        """
        Get child_id value
        """

        return self.get("child_id")

    @property
    def active(self) -> str:
        """
        Get active value
        """

        return self.get("active")

    @property
    def description(self) -> str:
        """
        Get description value
        """

        return self.get("description")

    @property
    def path(self) -> str:
        """
        Get path value
        """

        return self.get("path")

    @property
    def runtime(self) -> str:
        """
        Get runtime value
        """

        return self.get("runtime")

    @property
    def code(self) -> str:
        """
        Get code value
        """

        return self.get("code")

    @property
    def created_at(self) -> str:
        """
        Get created_at value
        """

        return self.get("created_at")

    @property
    def created_by(self) -> str:
        """
        Get created_by value
        """

        return self.get("created_by")

    @property
    def deleted_at(self) -> str:
        """
        Get deleted_at value
        """

        return self.get("deleted_at")

    @property
    def deleted_by(self) -> str:
        """
        Get deleted_by value
        """

        return self.get("deleted_by")
