"""Esquemas para los procesos"""
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.modules.docentes.schemas.schema import TeacherManagement
from app.modules.estudiantes.schemas.schema import StudentManagement
from app.modules.proceso.models.process import ProcessStatus, ProcessStage

class ProcessBase(BaseModel):
    id_student_program: int = Field(..., gt=0)
    id_adviser: int = Field(..., gt=0)
    current_thesis_title: str = Field(..., min_length=1)


class ProcessUpdate(BaseModel):
    current_thesis_title: str | None = Field(default=None, min_length=1)
    general_status: ProcessStatus | None = None
    current_stage: ProcessStage | None = None


class ProcessManagement(BaseModel):
    id: int
    student: StudentManagement
    teacher: TeacherManagement
    current_thesis_title: str
    general_status: ProcessStatus
    current_stage: ProcessStage
    start_date: datetime
    end_date: datetime | None

    model_config = ConfigDict(from_attributes=True)