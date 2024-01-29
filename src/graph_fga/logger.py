import logging
from functools import lru_cache
from server_grpc.settings import settings


LOGGER_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
}


@lru_cache()
def get_logger() -> logging.Logger:
    logger = logging.getLogger("graph_fga")
    logger.setLevel(LOGGER_LEVELS.get(settings.LOGGER_LEVEL.lower(), "info"))

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = get_logger()
