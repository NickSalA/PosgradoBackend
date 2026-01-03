"""Modelo de datos para la gestión de profesores."""
from enum import Enum
from datetime import date
from typing import ClassVar, Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

class StatusTeacher(str, Enum):
    ACTIVE = "activo"
    INACTIVE = "inactivo"
    WITH_LICENSE  = "con_licencia"

class AcademicDegree(str, Enum):
    MASTER = "magister"
    DOCTORATE = "doctorado"

class Teacher(SQLModel, table=True):
    __tablename__: ClassVar[str] = 'docente'

    id: Optional[int] = Field(default=None, sa_column=Column("id_docente", Integer, primary_key=True))
    dni: str = Field(sa_column=Column("dni", String(20), unique=True, nullable=False))
    name: str = Field(sa_column=Column("nombres", String(100), nullable=False))
    paternal_surname: str = Field(sa_column=Column("apellido_paterno", String(100), nullable=False))
    maternal_surname: str = Field(sa_column=Column("apellido_materno", String(100), nullable=False))
    academic_email: Optional[str] = Field(sa_column=Column("correo_academico", String(100), unique=True, nullable=True))
    personal_email: Optional[str] = Field(sa_column=Column("correo_personal", String(100), unique=True, nullable=True))
    phone: Optional[str] = Field(default=None, sa_column=Column("celular", String(15), nullable=True))
    academic_degree: AcademicDegree = Field(sa_column=Column("grado_academico", PgEnum(AcademicDegree, name="docente_grado_academico"), nullable=False))
    license_start_date: Optional[date] = Field(default=None, sa_column=Column("fecha_inicio_licencia", Date, nullable=True))
    license_end_date: Optional[date] = Field(default=None, sa_column=Column("fecha_fin_licencia", Date, nullable=True))
    status: StatusTeacher = Field(default=StatusTeacher.ACTIVE, sa_column=Column("estado", PgEnum(StatusTeacher, name="docente_estado"), nullable=False))

    __table_args__ = (
        CheckConstraint("celular ~ '^[0-9]{9}$'", name="chk_docente_celular"),
        CheckConstraint("dni ~ '^[0-9]{8}$'", name="chk_docente_dni"),
    )
