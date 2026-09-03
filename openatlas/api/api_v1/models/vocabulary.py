from typing import Dict
from uuid import UUID

from pydantic import Field

from openatlas.api.api_v1.models.util import BaseSchema


class VocabularyStandardQuery(BaseSchema):
    case_study: int | None = Field(
        None,
        description="Filter types by a specific case study ID.")


class VocabularyFlatItem(BaseSchema):
    id: int
    uuid: UUID
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


class VocabularyFlatResponse(BaseSchema):
    types: Dict[str, VocabularyFlatItem]


class VocabularyTreeItem(BaseSchema):
    id: int
    uuid: UUID
    name: str
    classes: list[str] | None = None
    children: list['VocabularyTreeItem'] = Field(default_factory=list)


class VocabularyTreeResponse(BaseSchema):
    standard: list[VocabularyTreeItem] = Field(default_factory=list)
    place: list[VocabularyTreeItem] = Field(default_factory=list)
    custom: list[VocabularyTreeItem] = Field(default_factory=list)
    value: list[VocabularyTreeItem] = Field(default_factory=list)
    system: list[VocabularyTreeItem] = Field(default_factory=list)
    tools: list[VocabularyTreeItem] = Field(default_factory=list)


class VocabularyStandardResponse(BaseSchema):
    results: list[VocabularyTreeItem] = Field(default_factory=list)
