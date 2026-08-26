from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Dict
from uuid import UUID

class VocabularyStandardQuery(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    case_study: UUID | int | None = Field(
        None,
        description="Filter types by a specific case study ID or UUID."
    )


# --- TYPES (FLACH) ---
class TypeFlatItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int
    name: str
    description: str | None = None
    image_id: int | None = None
    selectable: bool | None = None
    classes: list[str] | None = None
    first: int | None = None
    last: int | None = None
    root: list[int] | None = None
    subs: list[int] | None = None
    count: int | None = None
    count_subs: int | None = None
    category: str | None = None

class SystemTypesResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    # Key ist die Typ-ID als String, Value ist das FlatItem
    types: Dict[str, TypeFlatItem]

    # --- TYPES (BAUM) ---

class TypeTreeItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int
    name: str
    classes: list[str] | None = None
    children: list['TypeTreeItem'] = Field(default_factory=list)

class SystemTypeTreeResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    standard: list[TypeTreeItem] = Field(default_factory=list)
    place: list[TypeTreeItem] = Field(default_factory=list)
    custom: list[TypeTreeItem] = Field(default_factory=list)
    value: list[TypeTreeItem] = Field(default_factory=list)
    system: list[TypeTreeItem] = Field(default_factory=list)
class SystemStandardTypesResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    results: list[TypeTreeItem] = Field(default_factory=list)
