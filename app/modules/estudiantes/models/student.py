"""Modelo de datos para la gestión de estudiantes."""
from enum import Enum
from datetime import datetime
from typing import ClassVar, Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

class StatusStudent(str, Enum):
    ACTIVE = "activo"
    INACTIVE = "inactivo"

class TypeDocumentStudent(str, Enum):
    DNI = "dni"
    PASSPORT = "pasaporte"
    FOREIGN_IDENTITY = "cedula_identidad"

class Student(SQLModel, table=True):
    __tablename__: ClassVar[str] = 'estudiante'

    id: Optional[int] = Field(default=None, sa_column=Column("id_estudiante", Integer, primary_key=True))
    name: str = Field(sa_column=Column("nombre", String(100), nullable=False))
    paternal_surname: str = Field(sa_column=Column("apellido_paterno", String(100), nullable=False))
    maternal_surname: str = Field(sa_column=Column("apellido_materno", String(100), nullable=False))
    phone: Optional[str] = Field(default=None, sa_column=Column("celular", String(15), nullable=True))
    academic_email: Optional[str] = Field(sa_column=Column("correo_academico", String(100), unique=True, nullable=True))
    personal_email: Optional[str] = Field(sa_column=Column("correo_personal", String(100), unique=True, nullable=True))
    identity_document: str = Field(sa_column=Column("documento_identidad", String(20), unique=True, nullable=False))
    type_document: TypeDocumentStudent = Field(sa_column=Column("tipo_documento", PgEnum(TypeDocumentStudent, name="estudiante_tipo_documento"), nullable=False))
    nacionality: Optional[str] = Field(default=None, sa_column=Column("nacionalidad", String(100), nullable=True))
    status: StatusStudent = Field(sa_column=Column("estado", PgEnum(StatusStudent, name="estudiante_estado"), nullable=False))
    created_at: datetime = Field(default_factory=datetime.now ,sa_column=Column("fecha_creacion", DateTime, nullable=False))
    updated_at: Optional[datetime] = Field(default=None, sa_column=Column("fecha_modificacion", DateTime, nullable=True))

    __table_args__ = (
        CheckConstraint("celular ~ '^[0-9]{9}$'", name="chk_estudiante_celular"),
    )
