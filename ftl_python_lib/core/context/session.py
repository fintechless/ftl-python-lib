"""
Context for the SQLalchemy session
Contains the session
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ftl_python_lib.core.providers.mysql.engine import MySqlEngine


class SessionContext:
    """
    FTL Context about the session
    """

    def __init__(self) -> None:
        """
        Constructor
        """

    def get_session(self):
        Session = sessionmaker(bind=MySqlEngine.get_engine())
        session = Session()

        return session
