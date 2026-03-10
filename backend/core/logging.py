"""Централизованная настройка structlog + stdlib. Уровень из LOG_LEVEL в env."""

import logging
import os
import sys

import structlog


def _get_log_level() -> int:
    """Уровень логирования из env. DEBUG, INFO, WARNING, ERROR."""
    name = os.environ.get("LOG_LEVEL", "INFO").upper()
    return getattr(logging, name, logging.INFO)


def configure_logging() -> None:
    """
    Настраивает structlog с stdlib как backend.
    Все логи (structlog + uvicorn) идут в один поток через logging.
    """
    level = _get_log_level()

    # Общие процессоры для structlog
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # ProcessorFormatter для вывода structlog-событий
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.plain_traceback,
            ),
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    # uvicorn — пусть идёт через root
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        log = logging.getLogger(name)
        log.handlers.clear()
        log.propagate = True
