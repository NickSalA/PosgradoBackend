"""Modelo de datos para la gestión de Estudiantes matriculados en Programas."""
from enum import Enum
from typing import ClassVar, Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

class StatusStudentProgram(str, Enum):
    ACTIVE = "activo"
    INACTIVE = "inactivo"
    GRADUATED = "egresado"

class ProgramStudent(SQLModel, table=True):
    __tablename__: ClassVar[str] = 'programa_estudiante'

    id: Optional[int] = Field(default=None, sa_column=Column("id_programa_estudiante", Integer, primary_key=True))
    program_id: int = Field(sa_column=Column("id_programa", Integer, ForeignKey("programa.id_programa"),nullable=False))
    student_id: int = Field(sa_column=Column("id_estudiante", Integer, ForeignKey("estudiante.id_estudiante"), nullable=False))
    code: str = Field(sa_column=Column("codigo_alumno", String(8), unique=True, nullable=False))
    curriculum: int = Field(default=None, sa_column=Column("malla_curricular", Integer, nullable=True))
    status: StatusStudentProgram = Field(sa_column=Column("estado", PgEnum(StatusStudentProgram, name="programa_estudiante_estado"), nullable=False))
    admission_year: int = Field(sa_column=Column("fecha_inicio", Integer, nullable=False))
    graduation_year: Optional[int] = Field(default=None, sa_column=Column("fecha_fin", Integer, nullable=True))

    __table_args__ = (
        CheckConstraint("codigo_alumno ~ '^[0-9]{8}$'", name="chk_codigo_alumno"),
    )
