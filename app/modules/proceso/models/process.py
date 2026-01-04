"""Modelo de datos para la gestión de procesos."""
from enum import Enum
from typing import ClassVar, Optional

from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

class ProcessStatus(str, Enum):
    IN_PROCESS = "en_proceso"
    PAUSED = "pausado"
    FINALIZED = "finalizado"
    CANCELLED = "cancelado"

class ProcessStage(str, Enum):
    ENROLLMENT = "inscripcion"
    TURNITIN = "turnitin"
    CLEARED = "expedito"
    JURY_ASSIGNMENT = "designacion_jurados"
    PUBLIC_DEFENSE = "acto_publico"
    CYBERTESIS = "cybertesis"
    DEGREE_GRANTING = "otorgamiento_grado"
    SUNEDU_DIPLOMA = "diploma_sunedu"
    FINALIZED = "finalizado"

class Process(SQLModel, table=True):
    __tablename__: ClassVar[str] = 'proceso_tesis'

    id: Optional[int] = Field(default=None, sa_column=Column("id_proceso", Integer, primary_key=True))
    id_student_program: int = Field(sa_column=Column("id_estudiante_programa",Integer, ForeignKey("estudiante_programa.id_estudiante_programa"), nullable=False))
    id_advisor: int = Field(sa_column=Column("id_asesor",Integer, ForeignKey("docente.id_docente"), nullable=False))
    current_thesis_title: Optional[str] = Field(default=None, sa_column=Column("titulo_tesis_actual", Text, nullable=True))
    general_status: ProcessStatus = Field(default=ProcessStatus.IN_PROCESS, sa_column=Column("estado_general", PgEnum(ProcessStatus, name="proceso_tesis_estado_general"), nullable=False))
    current_stage: ProcessStage = Field(default=ProcessStage.ENROLLMENT, sa_column=Column("etapa_actual", PgEnum(ProcessStage, name="proceso_tesis_etapa_actual"), nullable=False))
    start_date: datetime = Field(sa_column=Column("fecha_inicio", DateTime(timezone=False), server_default=func.now(), nullable=False))
    end_date: Optional[datetime] = Field(default=None, sa_column=Column("fecha_finalizacion", DateTime(timezone=False), nullable=True))

    # Relationship a futuro
    # student_program: Optional["ProgramStudent"] = Relationship()
    # advisor: Optional["Teacher"] = Relationship()
