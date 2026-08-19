from datetime import date
from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class OpenAtlasClassEnum(str, Enum):
    ACQUISITION = 'acquisition'
    ACTIVITY = 'activity'
    # ADMINISTRATIVE_UNIT = 'administrative_unit'
    # ALIAS = 'alias'
    ARTIFACT = 'artifact'
    BIBLIOGRAPHY = 'bibliography'
    EDITION = 'edition'
    EXTERNAL_REFERENCE = 'external_reference'
    FEATURE = 'feature'
    FILE = 'file'
    GROUP = 'group'
    HUMAN_REMAINS = 'human_remains'
    MODIFICATION = 'modification'
    MOVE = 'move'
    # OBJECT_LOCATION = 'object_location'
    PERSON = 'person'
    PLACE = 'place'
    PRODUCTION = 'production'
    REFERENCE_SYSTEM = 'reference_system'
    SOURCE = 'source'
    STRATIGRAPHIC_UNIT = 'stratigraphic_unit'
    TEXT = 'text'
    TYPE = 'type'
    # TYPE_TOOLS = 'type_tools'


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
    entity_class: OpenAtlasClassEnum = Field(
        ...,
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
