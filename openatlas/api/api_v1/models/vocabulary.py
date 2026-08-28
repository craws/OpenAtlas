from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Dict


class VocabularyStandardQuery(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    case_study: int | None = Field(
        None,
        description="Filter types by a specific case study ID."
    )


class VocabularyFlatItem(BaseModel):
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


class VocabularyFlatResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    types: Dict[str, VocabularyFlatItem]


class VocabularyTreeItem(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int
    name: str
    classes: list[str] | None = None
    children: list['VocabularyTreeItem'] = Field(default_factory=list)


class VocabularyTreeResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    standard: list[VocabularyTreeItem] = Field(default_factory=list)
    place: list[VocabularyTreeItem] = Field(default_factory=list)
    custom: list[VocabularyTreeItem] = Field(default_factory=list)
    value: list[VocabularyTreeItem] = Field(default_factory=list)
    system: list[VocabularyTreeItem] = Field(default_factory=list)


class VocabularyStandardResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    results: list[VocabularyTreeItem] = Field(default_factory=list)
