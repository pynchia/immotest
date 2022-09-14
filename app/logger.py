import asyncio
import functools
import logging.config

from app.core.config import settings

LOGGER_NAME = "test"
LOG_FORMAT: str = "%(asctime)s|%(levelname)s|%(message)s"
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
LOG_LEVEL = LOG_LEVELS.get(settings.LOG_LEVEL, logging.ERROR)
LOGGING_CONFIG = {
    "version": 1,  # mandatory field
    "formatters": {
        "basic": {
            "format": LOG_FORMAT,
        }
    },
    "handlers": {
        "console": {
            "formatter": "basic",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": LOG_LEVEL,
        }
    },
    "loggers": {
        LOGGER_NAME: {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            # "propagate": False
        }
    },
}


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(LOGGER_NAME)


def log_call(func):
    """
    Decorator to allow tracing when a function is called
    and with which arguments
    """

    @functools.wraps(func)
    async def wrapper_async(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"{func.__name__} awaited with args {signature}")
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    @functools.wraps(func)
    def wrapper_sync(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"{func.__name__} called with args {signature}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper_async if asyncio.iscoroutinefunction(func) else wrapper_sync
