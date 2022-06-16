"""
Utility for logging purposes
"""

import logging
import logging.config


class Logging:
    """
    Main Logging class
    :param logfile: Local file where the logs will be written to
    """

    def __init__(self, logfile: str) -> None:
        logging.config.dictConfig(
            {
                "version": 1,
                "formatters": {
                    "default": {
                        "format": "[%(asctime)s] %(levelname)8s in %(module)s:%(lineno)s -- %(message)s",
                    }
                },
                "handlers": {
                    "wsgi": {
                        "class": "logging.StreamHandler",
                        "stream": "ext://flask.logging.wsgi_errors_stream",
                        "formatter": "default",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "stream": "ext://sys.stdout",
                        "formatter": "default",
                    },
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "formatter": "default",
                        "filename": logfile,
                        "maxBytes": 10485760,
                        "backupCount": 20,
                        "encoding": "utf8",
                    },
                },
                "loggers": {  # here you can add specific configuration for other libraries
                    "werkzeug": {
                        "level": "INFO",
                        "handlers": ["file", "console"],
                        "propagate": False,
                    }
                },
                "root": {
                    "level": logging.DEBUG,
                    "handlers": ["file", "console"],
                    "propagate": False,
                },
            }
        )

    @property
    def logger(self) -> logging:
        """
        Getter for logger
        """

        return logging


LOGGER: Logging = Logging(logfile="fintechless.log")
