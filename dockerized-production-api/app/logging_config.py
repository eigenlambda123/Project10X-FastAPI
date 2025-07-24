import logging
import os
from logging.handlers import RotatingFileHandler

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "plain")

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

def setup_logging():
    """
    Logging configuration
    """
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # Clear previous handlers
    logger.handlers.clear()

    # STDOUT handler
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    # Rotating file handler
    if os.getenv("LOG_TO_FILE") == "1":
        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=5_000_000, backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
