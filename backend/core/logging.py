"""Централизованная настройка structlog. Уровень из LOG_LEVEL в env."""

import logging
import os

import structlog


def _get_log_level() -> int:
    """Уровень логирования из env. DEBUG, INFO, WARNING, ERROR."""
    name = os.environ.get("LOG_LEVEL", "INFO").upper()
    return getattr(logging, name, logging.INFO)


def configure_logging() -> None:
    """Настраивает structlog. Вызывать при старте приложения."""
    level = _get_log_level()
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
    )
