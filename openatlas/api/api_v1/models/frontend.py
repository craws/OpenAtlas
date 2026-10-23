from uuid import UUID

from pydantic import Field

from openatlas.api.api_v1.models.lod import EntityCollectionQuery
from openatlas.api.api_v1.models.util import (
    BaseSchema, OpenAtlasClassEnum, TimeSpan)


class SearchQuery(EntityCollectionQuery):
    entity_class: OpenAtlasClassEnum | None = Field(
        None,
        description="Optional OpenAtlas system class filter.")


class SearchResultItem(BaseSchema):
    id: int
    uuid: UUID
    name: str
    system_class: str = Field(
        description="The OpenAtlas system class name.",
        examples=["place", "person"])
    description: str | None = None
    timespan: TimeSpan | None = None


class SearchResponse(BaseSchema):
    data: list[SearchResultItem] = Field(
        description="Page of matching search results.")
    total_items: int = Field(
        description="Total number of matching entities.")
    first: str = Field(description="URL to the first page of results.")
    previous: str | None = Field(
        None,
        description="URL to the previous page of results, if available.")
    next: str | None = Field(
        None,
        description="URL to the next page of results, if available.")
    last: str = Field(description="URL to the last page of results.")
