"""Aplicación principal de FastAPI para el backend de Posgrado."""

# Logging
import logging.config

# Context manager para lifespan
from contextlib import asynccontextmanager

# FastAPI y middlewares
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Uvicorn para correr la app
import uvicorn

# Configuración de logging
from app.core.logging_config import LOGGING_CONFIG

# Excepciones personalizadas
from app.core.exceptions import AppError

# Importar gestor de secretos
from app.core.config import get_secret

# Importar routers
from app.modules.estudiantes.controller.router import router as router_estudiantes
from app.modules.docentes.controller.router import router as router_docentes
from app.modules.dashboard_estudiantes.controller.router import router as router_dashboard_estudiantes
from app.modules.dashboard_docentes.controller.router import router as router_dashboard_docentes
from app.modules.inscripcion.controller.router import router as router_inscripcion
from app.modules.turnitin.controller.router import router as router_turnitin
from app.modules.expedito.controller.router import router as router_expedito
from app.modules.designacion_de_jurados.controller.router import router as router_designacion_jurados
from app.modules.acto_publico.controller.router import router as router_acto_publico
from app.modules.cybertesis.controller.router import router as router_cybertesis
from app.modules.otorgamiento.controller.router import router as router_otorgamiento

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Context manager para el ciclo de vida de la aplicación.
    """
    logger.info("Iniciando la aplicación Posgrado Backend...")
    yield
    logger.info("Cerrando la aplicación Posgrado Backend...")

app = FastAPI(title="Posgrado Backend API", version="1.0.0", lifespan=lifespan)

app.include_router(router_estudiantes, prefix="/module", tags=["Modulo", "Estudiantes"])
app.include_router(router_docentes, prefix="/module", tags=["Modulo", "Docentes"])
app.include_router(router_dashboard_estudiantes, prefix="/module", tags=["Dashboard","Estudiante"])
app.include_router(router_dashboard_docentes, prefix="/module", tags=["Dashboard","Docente"])
app.include_router(router_inscripcion, prefix="/stage", tags=["Inscripcion"])
app.include_router(router_turnitin, prefix="/stage", tags=["Turnitin"])
app.include_router(router_expedito, prefix="/stage", tags=["Expedito"])
app.include_router(router_designacion_jurados, prefix="/stage", tags=["Designacion de jurados"])
app.include_router(router_acto_publico, prefix="/stage", tags=["Acto publico"])
app.include_router(router_cybertesis, prefix="/stage", tags=["Cybertesis"])
app.include_router(router_otorgamiento, prefix="/stage", tags=["Otorgamiento"])

ALLOWED_ORIGINS = [
    "http://0.0.0.0:8000",
    "http://127.0.0.1:8000"
    ]

# CORS (ajusta origins a tu front real)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cookie de sesión
app.add_middleware(
    SessionMiddleware,
    secret_key=get_secret("SESSION-SECRET-KEY"),
    same_site="lax",
    https_only=False,   # pon True en producción HTTPS
    # session_cookie="support_session",
)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """
    Gestor global para excepciones de AppError.
    Args:
        request (Request): Objeto de la solicitud entrante.
        exc (AppError): Excepción capturada.
    Returns:
        JSONResponse: Respuesta JSON con detalles del error.
    """
    status_code = getattr(exc, "status_code", 500)
    method = request.method
    url = request.url.path
    request_id = request.headers.get("X-Request-ID", "Desconocido")
    ip = request.client.host if request.client else "Desconocida"

    log_message = f"[{request_id}] | {method} {url} | IP: {ip} | Error: {str(exc)}"

    if status_code >= 500:
        logger.error("CRITICO: %s", log_message)
    elif status_code >= 400:
        logger.warning("CLIENTE: %s", log_message)
    else:
        logger.info("INFO: %s", log_message)

    return JSONResponse(
        status_code=status_code,
        content={
            "error": True, 
            "type": exc.__class__.__name__, 
            "message": str(exc)},
    )

@app.get("/")
def home():
    """Endpoint raíz para verificar que la API está activa."""
    return {"ok": True, "msg": "API de Posgrado activa."}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)
