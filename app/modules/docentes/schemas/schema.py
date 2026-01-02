"""Esquemas para el módulo de docentes"""
from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.modules.docentes.models.teacher import StatusTeacher, AcademicDegree

class TeacherBase(BaseModel):
    dni: str = Field(..., max_length=20)
    name: str = Field(..., min_length=2, max_length=100)
    paternal_surname: str = Field(..., min_length=2, max_length=100)
    maternal_surname: str = Field(..., min_length=2, max_length=100)
    academic_degree: AcademicDegree = Field(..., max_length=20)
    status: StatusTeacher = Field(default=StatusTeacher.ACTIVE)

    # Campos opcionales
    academic_email: EmailStr | None = Field(default=None, max_length=100)
    personal_email: EmailStr | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=15)

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    academic_email: EmailStr | None = None
    personal_email: EmailStr | None = None
    phone: str | None = None
    status: StatusTeacher | None = None
    license_start_date: date | None = None
    license_end_date: date | None = None
    academic_degree: AcademicDegree | None = None

class TeacherManagement(TeacherBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TeacherDashboard(TeacherBase):
    id: int
    license_start_date: date | None = None
    license_end_date: date | None = None

    model_config = ConfigDict(from_attributes=True)
