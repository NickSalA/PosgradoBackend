from fastapi import APIRouter, HTTPException, Depends
from app.core.exceptions import AppError
from loguru import logger
router = APIRouter()

@router.get("/ping")
def ping():
    return {"status": "ok", "module": "estudiantes"}
