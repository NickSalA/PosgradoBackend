"""Aplicación principal de FastAPI para el backend de Posgrado."""
# Sistema
import sys

# Logging
import logging.config

# FastAPI
from fastapi import FastAPI
from pydantic import ValidationError

# Uvicorn para correr la app
import uvicorn

# Configuración de logging
from app.core.logging_config import LOGGING_CONFIG

# Excepciones personalizadas
from app.core.exceptions import AzureAuthError

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Importar gestor de secretos
try:
    from app.factory import create
    app: FastAPI = create()
    logger.debug("Configuración importada correctamente.")
except AzureAuthError as e:
    logger.exception("Error de autenticación con Azure Key Vault: %s", e)
    sys.exit(1)
except ValidationError as e:
    logger.exception("Error de validación en la configuración (Pydantic): %s", e)
    sys.exit(1)
except ValueError as e:
    logger.exception("Error de valor en la configuración: %s", e)
    sys.exit(1)
except Exception as e: # pylint: disable=broad-except
    logger.exception("Error inesperado al importar la configuración: %s", e)
    sys.exit(1)


@app.get("/")
def home():
    """Endpoint raíz para verificar que la API está activa."""
    return {"ok": True, "msg": "API de Posgrado activa."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)
