"""Modelo de datos para la gestión de Programas."""
from enum import Enum
from typing import ClassVar, Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

class StatusProgram(str, Enum):
    ACTIVE = "activo"
    INACTIVE = "inactivo"

class DegreeProgram(str, Enum):
    MASTER = "maestria"
    DOCTORATE = "doctorado"

class Program(SQLModel, table=True):
    __tablename__: ClassVar[str] = 'programa'

    id: Optional[int] = Field(default=None, sa_column=Column("id_programa", Integer, primary_key=True))
    name: str = Field(sa_column=Column("nombre", String(50), nullable=False))
    mention: Optional[str] = Field(default=None, sa_column=Column("mencion", String(100), nullable=True))
    degree: DegreeProgram = Field(sa_column=Column("grado", PgEnum(DegreeProgram, name="programa_grado"), nullable=False))
    status: StatusProgram = Field(sa_column=Column("estado", PgEnum(StatusProgram, name="programa_estado"), nullable=False))
