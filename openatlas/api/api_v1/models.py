from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class EntityPath(BaseModel):
    id: UUID = Field(..., description="Unique identifier of the entity")
    ext: str | None = Field(
        None,
        description="Optional file extension (.json, .ttl, .xml, .nt)",
        json_schema_extra={
            "examples": {
                "json": {"summary": "JSON-LD Format", "value": "json"},
                "turtle": {"summary": "Turtle Format", "value": "ttl"},
                "xml": {"summary": "RDF/XML Format", "value": "xml"},
                "ntriples": {"summary": "N-Triples Format", "value": "nt"}}})


class EntityCollectionPath(BaseModel):
    entity_class: str = Field(
        ...,
        description="CIDOC class (e.g. 'E21_Person') or System class to "
                    "filter the entities.",
        json_schema_extra={"example": "E21_Person"})
    ext: str | None = Field(
        None,
        description="Optional file extension (.json, .ttl, .xml, .nt)",
        json_schema_extra={
            "examples": {
                "json": {"summary": "JSON-LD Format", "value": "json"},
                "turtle": {"summary": "Turtle Format", "value": "ttl"},
                "xml": {"summary": "RDF/XML Format", "value": "xml"},
                "ntriples": {"summary": "N-Triples Format", "value": "nt"}}})


class EntityCollectionQuery(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    search: str | None = Field(
        None,
        description="Free-text search across entity Name, Description, "
                    "and Alias.")
    sort: Literal['asc', 'desc'] = Field(
        'asc',
        description="Ordering results ascending or descending.")
    limit: int = Field(
        100,
        ge=1,
        le=1000,
        description="Number of records to return (max 1000).")
    offset: int = Field(
        0,
        ge=0,
        description="Number of records to skip (for pagination).")
    begin_from: date | None = Field(
        None,
        description="Filter by begin date, starting from (YYYY-MM-DD).")
    begin_to: date | None = Field(
        None,
        description="Filter by begin date, up to (YYYY-MM-DD).")
    end_from: date | None = Field(
        None,
        description="Filter by end date, starting from (YYYY-MM-DD).")
    end_to: date | None = Field(
        None,
        description="Filter by end date, up to (YYYY-MM-DD).")
    case_study: UUID | None = Field(
        None,
        description="Filter entities belonging to a specific case study UUID.")


class LinkedArtResponse(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    context: str = Field(
        default="https://linked.art/ns/v1/linked-art.json",
        alias="@context")
    id: str
    type: str
    _label: str
