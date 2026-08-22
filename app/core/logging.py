import logging
import sys

from app.core.config import settings


def setup_logging() -> None:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()

    log_level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )

    root_logger.setLevel(log_level)

    root_logger.handlers.clear()

    root_logger.addHandler(handler)