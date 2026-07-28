from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EntityPath(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the entity")
    ext: str | None = Field(None, description="Optional file extension (.json, .ttl, .xml, etc.)")


class LinkedArtResponse(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    context: str = Field(
        default="https://linked.art/ns/v1/linked-art.json",
        alias="@context")
    id: str
    type: str
    _label: str
