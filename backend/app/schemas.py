from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# ---------- Templates ----------

class TemplateBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    subject: str = Field(min_length=1, max_length=500)
    body: str = Field(min_length=1)
    category: str | None = Field(default=None, max_length=100)
    variables: list[Any] = Field(default_factory=list)
    is_active: bool = True


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    subject: str | None = Field(default=None, min_length=1, max_length=500)
    body: str | None = Field(default=None, min_length=1)
    category: str | None = Field(default=None, max_length=100)
    variables: list[Any] | None = None
    is_active: bool | None = None


class TemplateRead(TemplateBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ---------- Partners ----------

class PartnerBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: str = Field(min_length=3, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    company: str | None = Field(default=None, max_length=255)
    contact_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PartnerCreate(PartnerBase):
    pass


class PartnerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = Field(
        default=None, min_length=3, max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )
    company: str | None = Field(default=None, max_length=255)
    contact_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    metadata: dict[str, Any] | None = None


class PartnerRead(PartnerBase):
    model_config = ConfigDict(from_attributes=True)

    # Sur le modèle ORM, la colonne "metadata" est exposée sous l'attribut `metadata_`
    # (`Partner.metadata` est le MetaData de SQLAlchemy).
    metadata: dict[str, Any] = Field(default_factory=dict, validation_alias="metadata_")
    id: int
    created_at: datetime
    updated_at: datetime
