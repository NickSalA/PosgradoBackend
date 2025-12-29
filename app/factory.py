"""Patrón Factory para crear la aplicación."""

# Logging
import logging.config

# Context manager para lifespan
from contextlib import asynccontextmanager

# FastAPI y middlewares
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# Configuración del sistema
from app.core.config import settings

# Configuración de logging
from app.core.logging_config import LOGGING_CONFIG

# Excepciones personalizadas
from app.core.exceptions import AppError

# Importar routers de feature modules
from app.feature_modules.dashboard_estudiantes.controller.router import router as router_dashboard_estudiantes
from app.feature_modules.dashboard_docentes.controller.router import router as router_dashboard_docentes
from app.feature_modules.inscripcion.controller.router import router as router_inscripcion
from app.feature_modules.turnitin.controller.router import router as router_turnitin
from app.feature_modules.expedito.controller.router import router as router_expedito
from app.feature_modules.designacion_de_jurados.controller.router import router as router_designacion_jurados
from app.feature_modules.acto_publico.controller.router import router as router_acto_publico
from app.feature_modules.cybertesis.controller.router import router as router_cybertesis
from app.feature_modules.otorgamiento.controller.router import router as router_otorgamiento

# Importar routers módulos
from app.modules.estudiantes.controller.router import router as router_estudiantes
from app.modules.docentes.controller.router import router as router_docentes
from app.modules.documentos.controller.router import router as router_documentos
from app.modules.proceso.controller.router import router as router_proceso
from app.modules.recordatorios.controller.router import router as router_recordatorios
from app.modules.tareas.controller.router import router as router_tareas

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("Factory")

def create() -> FastAPI:
    """Crea y configura la aplicación FastAPI."""

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        """
        Context manager para el ciclo de vida de la aplicación.
        """
        logger.info("Iniciando la aplicación Posgrado Backend...")
        yield
        logger.info("Cerrando la aplicación Posgrado Backend...")

    app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0", lifespan=lifespan)

    app.include_router(router_estudiantes, prefix=f"{settings.GLOBAL_PREFIX}/estudiantes", tags=["Estudiantes"])
    app.include_router(router_docentes, prefix=f"{settings.GLOBAL_PREFIX}/docentes", tags=["Docentes"])
    app.include_router(router_documentos, prefix=f"{settings.GLOBAL_PREFIX}/documentos", tags=["Documentos"])
    app.include_router(router_proceso, prefix=f"{settings.GLOBAL_PREFIX}/procesos", tags=["Procesos"])
    app.include_router(router_recordatorios, prefix=f"{settings.GLOBAL_PREFIX}/recordatorios", tags=["Recordatorios"])
    app.include_router(router_tareas, prefix=f"{settings.GLOBAL_PREFIX}/tareas", tags=["Tareas"])
    app.include_router(router_dashboard_estudiantes, prefix=f"{settings.DASHBOARD_PREFIX}/estudiantes", tags=["Dashboard: Estudiante"])
    app.include_router(router_dashboard_docentes, prefix=f"{settings.DASHBOARD_PREFIX}/docentes", tags=["Dashboard: Docente"])
    app.include_router(router_inscripcion, prefix=f"{settings.STAGE_PREFIX}/inscripcion", tags=["Inscripcion"])
    app.include_router(router_turnitin, prefix=f"{settings.STAGE_PREFIX}/turnitin", tags=["Turnitin"])
    app.include_router(router_expedito, prefix=f"{settings.STAGE_PREFIX}/expedito", tags=["Expedito"])
    app.include_router(router_designacion_jurados, prefix=f"{settings.STAGE_PREFIX}/designacion_de_jurados", tags=["Designacion de jurados"])
    app.include_router(router_acto_publico, prefix=f"{settings.STAGE_PREFIX}/acto_publico", tags=["Acto publico"])
    app.include_router(router_cybertesis, prefix=f"{settings.STAGE_PREFIX}/cybertesis", tags=["Cybertesis"])
    app.include_router(router_otorgamiento, prefix=f"{settings.STAGE_PREFIX}/otorgamiento", tags=["Otorgamiento"])

    # CORS (ajusta origins a tu front real)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Cookie de sesión
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
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

    return app
