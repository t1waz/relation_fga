import os
from functools import lru_cache
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    MAX_WORKERS: int
    LOGGER_LEVEL: str
    GRAPH_DB_HOST: str
    GRAPH_DB_PORT: str


@lru_cache()
def get_settings():
    return Settings(
        GRAPH_DB_HOST=os.getenv("GRAPH_DB_HOST"),
        GRAPH_DB_PORT=os.getenv("GRAPH_DB_PORT"),
        MAX_WORKERS=int(os.getenv("MAX_WORKERS", 4)),
        LOGGER_LEVEL=os.getenv("LOGGER_LEVEL", "DEBUG"),
    )


settings = get_settings()
