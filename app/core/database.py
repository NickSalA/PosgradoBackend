"""Conexión a la base de datos y gestión de sesiones."""

# Logging
import logging.config

# SQLAlchemy y SQLModel
from sqlmodel import Session, create_engine
from sqlalchemy.exc import OperationalError, IntegrityError, SQLAlchemyError

# Configuración de logging
from app.core.logging_config import LOGGING_CONFIG

# Excepciones personalizadas
from app.core.exceptions import DatabaseConnectionError, DatabaseQueryError, DatabaseIntegrityError

# Importar configuración
from app.core.config import settings

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

DATABASE_URL: str = settings.DATABASE_URL

try:
    # Si es SQLite (para tests), no usamos sslmode
    connect_args = {}
    if DATABASE_URL and not str(DATABASE_URL).startswith("sqlite"):
        connect_args = {"sslmode": "require"}

    engine = create_engine(
        DATABASE_URL, echo=False, future=True,
        pool_pre_ping=True, connect_args=connect_args
        )
except OperationalError as e:
    logger.critical("Error fatal al configurar la conexión a la BD.")
    raise DatabaseConnectionError("Error de configuración a la BD.") from e

def get_session():
    """Proporciona una sesión de base de datos."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
            logger.debug("Sesión de base de datos comprometida exitosamente.")

        except IntegrityError as e:
            session.rollback()
            logger.warning("Error de integridad en la BD, realizando rollback.")
            raise DatabaseIntegrityError("Violación de integridad en la BD.") from e

        except OperationalError as e:
            session.rollback()
            logger.exception("Error de conexión a la BD durante la sesión, realizando rollback.")
            raise DatabaseConnectionError("Error de conexión a la BD.") from e

        except SQLAlchemyError as e:
            session.rollback()
            logger.exception("Error durante la sesión de BD, realizando rollback.")
            raise DatabaseQueryError("Error al ejecutar la consulta en la BD.") from e

        except Exception:
            session.rollback()
            logger.exception("Error inesperado durante la sesión de BD, realizando rollback.")
            raise
