"""Modelo de datos para categorías de documentos externos."""
from typing import ClassVar, Optional

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, Boolean


class ExternalDocumentCategory(SQLModel, table=True):
    __tablename__: ClassVar[str] = "cat_documento_externo"

    id: Optional[int] = Field(default=None, sa_column=Column("id_cat_doc_ext", Integer, primary_key=True))
    full_name: Optional[str] = Field(default=None, sa_column=Column("nombre_completo", String(200), nullable=True))
    is_active: Optional[bool] = Field(default=None, sa_column=Column("estado_activo", Boolean, nullable=True))
