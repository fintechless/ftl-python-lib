"""
Constants for Member
"""

from enum import Enum


class ConstantsMemberRole(Enum):
    """
    Member dictionary class - inherits the Enum class
    """

    OWNER = "owner"
    MANAGER = "manager"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
