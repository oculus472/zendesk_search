import logging
from logging import Logger

__all__ = ["set_log_level", "get_logger"]

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S, %d-%m-%Y",
)
_logger = logging.getLogger("zendesk_search")


def set_log_level(level: int) -> None:
    log_level = level * 10
    _logger.setLevel(log_level)


def get_logger() -> Logger:
    return _logger
