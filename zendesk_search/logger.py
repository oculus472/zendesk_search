import logging
from logging import Logger

__all__ = ["set_log_level", "get_logger"]

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S, %d-%m-%Y",
)
_logger = logging.getLogger("zendesk_search")


def set_log_level(level: int) -> None:
    """Set the log level for our global logger.

    Args:
        level (int): the level to set logging to.
    """
    log_level = level * 10
    _logger.setLevel(log_level)


def get_logger() -> Logger:
    """Get the global Zendesk logger instance."""
    return _logger
