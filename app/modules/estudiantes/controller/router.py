from fastapi import APIRouter, HTTPException, Depends

router = APIRouter()

@router.get("/ping")
def ping():
    return {"status": "ok", "module": "estudiantes"}