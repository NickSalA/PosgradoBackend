"""Modelo de datos para documentos externos asociados a un proceso."""
from enum import Enum
from typing import ClassVar, Optional
from datetime import date
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

class ReceptionStatus(str, Enum):
    RECIBIDO = "recibido"
    NO_RECIBIDO = "no_recibido"

class DeliveryStatus(str, Enum):
    ENTREGADO = "entregado"
    NO_ENTREGADO = "no_entregado"

class ExternalProcessDocument(SQLModel, table=True):
    __tablename__: ClassVar[str] = "documento_externo_proceso"

    id: Optional[int] = Field(default=None, sa_column=Column("id_doc_ext_proceso", Integer, primary_key=True))
    id_process: int = Field(sa_column=Column("id_proceso", Integer, ForeignKey("proceso_tesis.id_proceso"), nullable=False))
    id_process_stage: int = Field(sa_column=Column("id_etapa_proceso", Integer, ForeignKey("etapa_proceso.id_etapa_proceso"), nullable=False))
    id_external_doc_category: int = Field(sa_column=Column("id_cat_doc_ext", Integer, ForeignKey("cat_documento_externo.id_cat_doc_ext"), nullable=False))
    id_reception_task: int = Field(sa_column=Column("id_tarea_recepcion", Integer, ForeignKey("tarea.id_tarea"), nullable=False))
    id_delivery_task: int = Field(sa_column=Column("id_tarea_entrega", Integer, ForeignKey("tarea.id_tarea"), nullable=False))

    actor_emitter: Optional[str] = Field(default=None, sa_column=Column("actor_emisor", String(50), nullable=True))
    actor_addressee: Optional[str] = Field(default=None, sa_column=Column("actor_destinatario", String(50), nullable=True))
    reception_status: Optional[ReceptionStatus] = Field(default=None, sa_column=Column("estado_recepcion", PgEnum(ReceptionStatus, name="documento_externo_proceso_estado_recepcion"), nullable=True))
    delivery_status: Optional[DeliveryStatus] = Field(default=None, sa_column=Column("estado_entrega", PgEnum(DeliveryStatus, name="documento_externo_proceso_estado_entrega"), nullable=True))
    reception_date: Optional[date] = Field(default=None, sa_column=Column("fecha_recepcion", Date, nullable=True))
    delivery_date: Optional[date] = Field(default=None, sa_column=Column("fecha_entrega", Date, nullable=True))

    # Relationships a futuro
    # process: Optional["Process"] = Relationship()
    # stage: Optional["ProcessStage"] = Relationship()
    # category: Optional["ExternalDocumentCategory"] = Relationship()
    # reception_task: Optional["Task"] = Relationship()
    # delivery_task: Optional["Task"] = Relationship()
