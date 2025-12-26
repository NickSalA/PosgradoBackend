"""Módulo de excepciones personalizadas para la aplicación."""
class AppError(Exception):
    """Clase base para errores de la aplicación."""
    status_code = 400

# Errores específicos para la gestión de secretos en Azure Key Vault
class SecretNotFoundError(AppError):
    """Error cuando un secreto no es encontrado en Azure Key Vault."""
    status_code = 404

class SecretEmptyError(AppError):
    """Error cuando un secreto obtenido está vacío."""
    status_code = 400

class AzureAuthError(AppError):
    """Error de autenticación con Azure."""
    status_code = 503


#Errores genericos de la base de datos
class DatabaseConnectionError(AppError):
    """Error al conectar con la base de datos."""
    status_code = 503

class DatabaseQueryError(AppError):
    """Error genérico de SQL (sintaxis, tablas rotas, etc)."""
    status_code = 500

class DatabaseIntegrityError(AppError):
    """Error especifico para cuando el usuario viola una regla"""
    status_code = 409
