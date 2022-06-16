"""
Constants for Microservice
"""

from enum import Enum


class ConstantsMicroserviceMapping(Enum):
    """
    Microservice dictionary class - inherits the Enum class
    """

    DEPLOY = [
        "iac",
        ".codeclimate.yml",
        ".dockercontainers",
        ".terrahub.yml",
        "CODEOWNERS",
    ]
    BUILD = [
        "bin",
        ".codeclimate.yml",
        ".dockercontainers",
        ".dockerignore",
        "Dockerfile",
        "docker-compose.yml",
    ]
    TEST = [
        "tests",
        ".codeclimate.yml",
        ".pylintrc",
        "poetry.lock",
        "poetry.toml",
        "poetry",
        "pyproject.toml",
        "setup.cfg",
        "setup.py",
    ]
    CODE = [
        "RETRIEVED",
        ".codeclimate.yml",
        ".pylintrc",
        "LICENSE",
        "README.md",
        "ftl_msa_",
        "poetry.lock",
        "poetry.toml",
        "poetry",
        "pyproject.toml",
        "setup.cfg",
        "setup.py",
    ]
    MONITOR = []


class ConstantsMicroserviceDefault(Enum):
    """
    Microservice dictionary class - inherits the Enum class
    """

    DEFAULT = [".terrahub.yml", "Dockerfile", "conftest.py", "README.md"]
