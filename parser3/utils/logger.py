"""Small logging helper."""

from __future__ import annotations

import logging
from parser3.utils.constants import APP_NAME


def get_logger(name: str | None = None) -> logging.Logger:
    logger_name = name or APP_NAME
    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s | %(name)s | %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
