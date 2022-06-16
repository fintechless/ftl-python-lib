"""Create database connection."""
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from ftl_python_lib.core.context.environment import EnvironmentContext

ENVIRON_CONTEXT: EnvironmentContext = EnvironmentContext()


class MySqlEngine:
    """
    Engine
    """

    @staticmethod
    def get_connection_string() -> str:
        return (
            "mysql+pymysql://"
            + ENVIRON_CONTEXT.ftl_db_username
            + ":"
            + ENVIRON_CONTEXT.ftl_db_password
            + "@"
            + ENVIRON_CONTEXT.ftl_db_host
            + "/"
            + ENVIRON_CONTEXT.ftl_db_database
        )

    @staticmethod
    def get_engine() -> Engine:
        engine = create_engine(MySqlEngine.get_connection_string(), echo=True)

        return engine
