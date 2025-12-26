"""Gestor de Secretos de Azure Key Vault."""
# Logging
import logging
import logging.config

# Credenciales Azure
from azure.identity import DefaultAzureCredential

# Manejo de secretos en Key Vault
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError

# Exceptions
from app.core.exceptions import SecretNotFoundError, SecretEmptyError, AzureAuthError

# Configuración de logging
from app.core.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")

VAULT_NAME = "posgrado"
KV_URL = f"https://{VAULT_NAME}.vault.azure.net"

try:
    logger.info("Obteniendo credenciales de Azure Key Vault...")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KV_URL, credential=credential)
    logger.debug("Credenciales obtenidas correctamente.")

except Exception as e:
    logger.exception("Error al obtener credenciales de Azure Key Vault.")
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
