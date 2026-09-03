from typing import Any, Literal
from uuid import UUID

from pydantic import ConfigDict, Field, field_validator

from openatlas.api.api_v1.models.util import BaseSchema, ExtensionsType, \
    OpenAtlasClassEnum
from openatlas.api.api_v1.util.date_util import handle_date


class EntityPath(BaseSchema):
    id: UUID = Field(..., description="Unique identifier of the entity")


class EntityPathExt(BaseSchema):
    id: UUID = Field(..., description="Unique identifier of the entity")
    ext: ExtensionsType = Field(
        ...,
        description="File extension (.json, .ttl, .xml, .nt)",
        json_schema_extra={
            "examples": {
                "json": {"summary": "JSON-LD Format", "value": "json"},
                "turtle": {"summary": "Turtle Format", "value": "ttl"},
                "xml": {"summary": "RDF/XML Format", "value": "xml"},
                "ntriples": {"summary": "N-Triples Format", "value": "nt"}}})


class EntityCollectionPath(BaseSchema):
    entity_class: OpenAtlasClassEnum = Field(
        ...,
        alias="entity_class",
        description="Choose one of the following classes: ",
        json_schema_extra={
            "examples": {
                "person": {
                    "summary": "Person (E21 Person)",
                    "value": "person"},
                "group": {
                    "summary": "Group (E74 Group)",
                    "value": "group"},
                "artifact": {
                    "summary": "Artifact (E22 Human-Made Object)",
                    "value": "artifact"},
                "place": {
                    "summary": "Place (E18 Physical Thing)",
                    "value": "place"},
                "activity": {
                    "summary": "Activity (E7 Activity)",
                    "value": "activity"},
                "acquisition": {
                    "summary": "Acquisition (E8 Acquisition)",
                    "value": "acquisition"},
                "move": {
                    "summary": "Move (E9 Move)",
                    "value": "move"},
                "modification": {
                    "summary": "Modification (E11 Modification)",
                    "value": "modification"},
                "production": {
                    "summary": "Production (E12 Production)",
                    "value": "production"},
                "source": {
                    "summary": "Source (E33 Linguistic Object)",
                    "value": "source"},
                "bibliography": {
                    "summary": "Bibliography (E31 Document)",
                    "value": "bibliography"},
                "file": {
                    "summary": "File (E31 Document)",
                    "value": "file"},
                "administrative_unit": {
                    "summary": "Admin Unit (E53 Place)",
                    "value": "administrative_unit"},
                "feature": {
                    "summary": "Feature (E18 Physical Thing)",
                    "value": "feature"},
                "human_remains": {
                    "summary": "Human Remains (E20 Biological Object)",
                    "value": "human_remains"},
                "stratigraphic_unit": {
                    "summary": "Stratigraphic Unit (E18 Physical Thing)",
                    "value": "stratigraphic_unit"},
                "type": {
                    "summary": "Type (E55 Type)",
                    "value": "type"}}})


class EntityCollectionQuery(BaseSchema):
    search: str | None = Field(
        None,
        description="Filter entities by name (case-insensitive substring "
                    "match).")
    sort_by: Literal['name', 'start_date', 'end_date'] = Field(
        'name',
        description="Field to sort by: 'name', 'startDate', or 'endDate'.")
    sort: Literal['asc', 'desc'] = Field(
        'asc',
        description="Sort direction: 'asc' or 'desc'.")
    limit: int = Field(
        50,
        ge=1,
        le=100,
        description="Number of records to return (max 100).")
    page: int = Field(
        1,
        ge=1,
        description="Page number (starting at 1).")
    start_date: str | None = Field(
        None,
        description="Filter entities with begin date on or after this date ("
                    "e.g. 0400-01-01, 400, -400).")
    end_date: str | None = Field(
        None,
        description="Filter entities with end date on or before this date ("
                    "e.g. 0400-12-31, 400, -400).")
    type_id: int | UUID | str | None = Field(
        None,
        description="Filter entities by type ID (integer) or type UUID.")
    case_study: int | UUID | str | None = Field(
        None,
        description="Filter entities by case study ID (integer) or case "
                    "study UUID.")

    @field_validator('sort_by', mode='before')
    @classmethod
    def validate_sort_by(cls, value: Any) -> str:
        if value in ('startDate', 'start_date'):
            return 'start_date'
        if value in ('endDate', 'end_date'):
            return 'end_date'
        return value

    @field_validator('start_date', mode='before')
    @classmethod
    def validate_start_date(cls, value: Any) -> str | None:
        if value is None:
            return None
        return handle_date(value, is_end_date=False)

    @field_validator('end_date', mode='before')
    @classmethod
    def validate_end_date(cls, value: Any) -> str | None:
        if value is None:
            return None
        return handle_date(value, is_end_date=True)


class LinkedArtResponse(BaseSchema):
    model_config = ConfigDict(extra='allow')

    context: str = Field(
        default="https://linked.art/ns/v1/linked-art.json",
        alias="@context")
    id: str
    type: str
    _label: str


class LinkedArtCollectionResponse(BaseSchema):
    model_config = ConfigDict(extra='allow')

    context: list[str | dict[str, str]] = Field(
        default=[
            "https://linked.art/ns/v1/linked-art.json",
            {"hydra": "http://www.w3.org/ns/hydra/core#"}],
        alias="@context")
    id: str
    type: str = "hydra:PartialCollectionView"
    total_items: int = Field(alias="hydra:totalItems")
    first: str = Field(alias="hydra:first")
    previous: str | None = Field(default=None, alias="hydra:previous")
    next: str | None = Field(default=None, alias="hydra:next")
    last: str = Field(alias="hydra:last")
    graph: list[dict[str, Any]] = Field(alias="@graph")
