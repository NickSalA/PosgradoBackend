from fastapi import APIRouter, HTTPException, Depends
from app.core.exceptions import AppError
from loguru import logger
router = APIRouter()

@router.get("/ping")
def ping():
    return {"status": "ok", "module": "estudiantes"}

@router.get("/{student_id}")
def get_student(student_id: int):
    return {"student_id": student, "name": "John Doe"} 