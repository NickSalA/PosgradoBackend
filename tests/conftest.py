"""Herramientas para probar la aplicación."""

# Pytest para fixtures y testing
import pytest
from fastapi.testclient import TestClient

# SQLModel para la base de datos de pruebas
from sqlmodel import create_engine, StaticPool, SQLModel, Session

# Importar la aplicación FastAPI
from app.main import app

# Importar la función para obtener la sesión de la base de datos
from app.core.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    """
    Proporciona una sesión de base de datos para las pruebas.
    """
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Proporciona un cliente de prueba para la aplicación FastAPI.
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
