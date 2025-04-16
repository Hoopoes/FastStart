import os
import logging
from config import CONFIG
from logging.config import dictConfig

from app.core.log_handler import LOG_DIRECTORY

# Logging configuration
log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "app.core.log_handler.JsonFormatter",  # JSON logs for Grafana Loki
        },
    },
    "filters": {
        "context_filter": {
            "()": "app.core.log_handler.ContextLogFilter"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
            "filters": ["context_filter"]
        },
        "file": {
            "class": "app.core.log_handler.CustomTimedRotatingFileHandler",
            "formatter": "json",
            "filename": os.path.join(LOG_DIRECTORY, "today.log"),
            "when": "midnight",
            "backupCount": 7,
            "encoding": "utf-8",
            "filters": ["context_filter"]
        },
    },
    "loggers": {
        f"{CONFIG.app_name}": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Configure logging
dictConfig(log_config)

# Define a logger
LOG = logging.getLogger(f"{CONFIG.app_name}")

# Test logging
LOG.info(f"{CONFIG.app_name} logger initialized")
