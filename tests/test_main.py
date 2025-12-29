import pytest
from fastapi.testclient import TestClient
from app.factory import create
from app.core.config import settings

# 1. Creamos una instancia de la app usando tu Factory
# Esto simula el arranque sin necesidad de correr uvicorn
app = create()

# 2. Creamos el cliente de pruebas (es como un navegador fake)
client = TestClient(app)

def test_root_endpoint():
    """
    Verifica que el endpoint raíz '/' definido en factory.py funcione.
    """
    response = client.get("/")
    assert response.status_code == 200
    
    # Verificamos el contenido del JSON
    data = response.json()
    assert data["ok"] is True
    assert "msg" in data

def test_swagger_ui_exists():
    """
    Verifica que la documentación automática se genere (significa que la app montó bien).
    """
    response = client.get("/docs")
    assert response.status_code == 200

def test_global_prefix_configuration():
    """
    Verifica que la configuración GLOBAL_PREFIX se esté aplicando a los routers.
    Intentamos acceder a una ruta que sabemos que existe en ese prefijo.
    """
    # Usamos el prefijo real de tu configuración
    prefix = settings.GLOBAL_PREFIX 
    
    # Intentamos acceder a un endpoint de estudiantes (aunque sea 401/403 o 404,
    # lo importante es que NO sea 404 por "Ruta no encontrada", sino por lógica de negocio)
    # Si la ruta base está mal montada, esto daría 404 directo.
    
    # Nota: Como no tenemos token aquí, podría dar 401 o 403, 
    # pero verificamos que NO sea 404 (Not Found) en la raíz del módulo.
    
    # Ejemplo: Ver si el router de estudiantes está montado
    # Asumimos que tienes un endpoint GET en estudiantes, si no, ajusta la ruta
    response = client.get(f"{prefix}/estudiantes/ping") 
    
    # Si tu API requiere autenticación, probablemente recibas un 401 o 403.
    # Si recibes 404, significa que el router NO se montó en esa URL.
    assert response.status_code != 404

def test_cors_headers():
    """
    Verifica que los headers de CORS se estén inyectando.
    """
    response = client.get("/", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"

def test_app_title():
    """
    Verifica que el título se haya cargado desde la configuración.
    """
    assert app.title == settings.PROJECT_NAME