"""Esquemas para los documentos"""
from pydantic import BaseModel, ConfigDict, Field
from app.modules.documentos.models.document import ReceptionStatus, DeliveryStatus
from datetime import date

class DocumentBase(BaseModel):
    actor_emitter: str = Field(..., min_length=1, max_length=50)
    actor_addressee: str = Field(..., min_length=1, max_length=50)
    reception_date: date | None = Field(default=None)
    delivery_date: date | None = Field(default=None)


class DocumentUpdate(BaseModel):
    actor_emitter: str | None = Field(default=None, max_length=50)
    actor_addressee: str | None = Field(default=None, max_length=50)
    reception_status: ReceptionStatus | None = None
    delivery_status: DeliveryStatus | None = None
    reception_date: date | None = None
    delivery_date: date | None = None


class CatalogDocument(BaseModel):
    id_cat_doc_ext: int
    full_name: str
    active_status: bool


class DocumentManagement(BaseModel):
    id: int
    id_process: int
    id_stage_process: int
    catalog_document: CatalogDocument
    id_task_reception: int
    id_task_delivery: int
    sender_actor: str | None
    recipient_actor: str | None
    reception_status: ReceptionStatus
    delivery_status: DeliveryStatus
    reception_date: date | None
    delivery_date: date | None

    model_config = ConfigDict(from_attributes=True)