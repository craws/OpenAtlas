from typing import Dict
from uuid import UUID

from pydantic import Field

from openatlas.api.api_v1.models.files import FileItem
from openatlas.api.api_v1.models.util import BaseSchema, \
    TimeSpan, ExternalReferenceSystemModel, ReferenceModel, TypeCategoryEnum


class VocabularyStandardQuery(BaseSchema):
    case_study: int | None = Field(
        None,
        description="Filter types by a specific case study ID.")


class LinkedTypeItem(BaseSchema):
    id: int
    name: str


class VocabularyFlatItem(BaseSchema):
    id: int
    uuid: UUID
    name: str
    class_name: str = Field(
        default="type",
        serialization_alias="class",
        description="The OpenAtlas class.")
    category: TypeCategoryEnum | None = Field(
        default=None,
        description="Categorization of the type.")
    description: str | None = None
    image: FileItem | None = Field(
        default=None,
        description="Primary representative image for the type.")
    selectable: bool = Field(
        default=True,
        description="Whether this type can be directly assigned to an "
                    "entity or serves only as a structural grouping node.")
    classes: list[str] = Field(
        default_factory=list,
        description="Entity classes this type can be assigned to "
                    "(e.g. 'artifact', 'place').",
        examples=[["artifact", "source"]])
    timespan: TimeSpan | None = Field(
        default=None,
        description="Temporal validity or usage period.")
    parents: list[LinkedTypeItem] = Field(
        default_factory=list,
        description="Immediate parent types for breadcrumbs.")
    sub_types: list[LinkedTypeItem] = Field(
        default_factory=list,
        description="Direct sub-types under this node.")
    entity_count: int = Field(
        default=0,
        description="Number of entities directly linked to this exact type.")
    entity_count_subs: int = Field(
        default=0,
        description="Number of entities linked to any of its descendants.")
    external_references: list[ExternalReferenceSystemModel] = Field(
        default_factory=list,
        description="Links to external authority systems "
                    "(Wikidata, Getty AAT, etc.).")
    references: list[ReferenceModel] = Field(
        default_factory=list,
        description="Bibliographic references and literature citations.")


class VocabularyFlatResponse(BaseSchema):
    types: Dict[str, VocabularyFlatItem]


class VocabularyTreeItem(BaseSchema):
    id: int
    uuid: UUID
    name: str
    selectable: bool = Field(
        default=True,
        description="Whether this node can be selected/assigned or serves "
                    "only as a category folder.")
    classes: list[str] = Field(
        default_factory=list,
        description="Entity classes this type is valid for.")
    entity_count: int = Field(
        default=0,
        description="Number of entities directly linked to this exact type.")
    entity_count_subs: int = Field(
        default=0,
        description="Number of entities linked to any of its descendants.")
    children: list["VocabularyTreeItem"] = Field(
            default_factory=list,
            description="Nested child nodes.")


class VocabularyTreeResponse(BaseSchema):
    standard: list[VocabularyTreeItem] = Field(default_factory=list)
    place: list[VocabularyTreeItem] = Field(default_factory=list)
    custom: list[VocabularyTreeItem] = Field(default_factory=list)
    value: list[VocabularyTreeItem] = Field(default_factory=list)
    system: list[VocabularyTreeItem] = Field(default_factory=list)
    tools: list[VocabularyTreeItem] = Field(default_factory=list)


class VocabularyStandardResponse(BaseSchema):
    results: list[VocabularyTreeItem] = Field(default_factory=list)
