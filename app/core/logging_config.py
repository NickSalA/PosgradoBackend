"""Configuración de logging para la aplicación."""

# Variables de entorno
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,     

    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "detailed",
            "filename": "app.log",
            "maxBytes": 10485760, # 10MB
            "backupCount": 5,
            "encoding": "utf8"
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": False
        },

        # Librerias
        "azure": {
            "level": "WARNING",
        },
        "urllib3": { 
            "level": "WARNING"
        },
    },

    # Logger por defecto
    "root": {
        "handlers": ["console", "file"],
        "level": "WARNING",
    }
}
