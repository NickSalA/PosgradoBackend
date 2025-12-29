"""Gestor de Secretos de Azure Key Vault."""
# Logging
import logging
import logging.config

# Credenciales Azure
from azure.identity import DefaultAzureCredential

# Manejo de secretos en Key Vault
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError

# Pydantic Settings
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Exceptions
from app.core.exceptions import SecretNotFoundError, SecretEmptyError, AzureAuthError

# Configuración de logging
from app.core.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

VAULT_NAME = "posgrado"
KV_URL = f"https://{VAULT_NAME}.vault.azure.net"

try:
    logger.debug("Obteniendo credenciales de Azure Key Vault...")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KV_URL, credential=credential)
    logger.debug("Credenciales obtenidas correctamente.")

except Exception as e:
    raise AzureAuthError("Error al obtener credenciales de Azure Key Vault.") from e

def get_secret(name: str) -> str:
    """
    Recupera el valor de un secreto desde Azure Key Vault.
    Args:
        name (str): Nombre del secreto a recuperar.
    Returns:
        str: Valor del secreto.
    """
    logger.debug("Obteniendo secreto: %s", name)
    try:
        secret = client.get_secret(name)
        if secret.value is None:
            logger.error("Secreto %s fue encontrado como None", name)
            raise SecretEmptyError(f"Secreto {name} no tiene un valor.")
        return secret.value
    except ResourceNotFoundError as e:
        logger.error("Secreto %s no encontrado en Key Vault.", name)
        raise SecretNotFoundError(f"Secreto {name} no encontrado en Key Vault.") from e
    except ClientAuthenticationError as e:
        logger.exception("Error de autenticación al acceder a Key Vault. Expira el token o credenciales inválidas.")
        raise AzureAuthError("Error de autenticación al acceder a Key Vault.") from e
    except Exception:
        logger.exception("Error inesperado al obtener el secreto: %s", name)
        raise

class Settings(BaseSettings):
    PROJECT_NAME: str = "Posgrado Backend API"
    GLOBAL_PREFIX: str = "/api/v1"
    STAGE_PREFIX: str = f"{GLOBAL_PREFIX}/stage"
    DASHBOARD_PREFIX: str = f"{GLOBAL_PREFIX}/dashboard"
    CORS_ORIGINS: list[str] = ["http://localhost:8000", "http://localhost:3000"]

    DATABASE_NAME: str = Field(default_factory=lambda: get_secret("DATABASE-NAME"))
    DATABASE_PASSWORD: str = Field(default_factory=lambda: get_secret("DATABASE-PASSWORD"))
    DATABASE_USER: str = Field(default_factory=lambda: get_secret("DATABASE-USER"))
    DATABASE_HOST: str = Field(default_factory=lambda: get_secret("DATABASE-HOST"))
    DATABASE_PORT: int = Field(default_factory=lambda: int(get_secret("DATABASE-PORT")))

    SECRET_KEY: str = Field(default_factory=lambda: get_secret("SESSION-SECRET-KEY"))
    LOG_LEVEL: str = "INFO"

    @property
    def DATABASE_URL(self) -> str:  # pylint: disable=invalid-name
        """Recupera la URL de la base de datos desde Key Vault o variable de entorno."""
        if not self.DATABASE_HOST:
            return "sqlite:///./test.db"
        return f"postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}?sslmode=require"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
