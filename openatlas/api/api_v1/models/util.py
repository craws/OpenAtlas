from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def convert_string_nulls_to_none(cls, data: Any) -> Any:
        """
        Convert string representations of "null" to None in a given input.
        Needed for Schemathesis to work properly.
        """

        if isinstance(data, dict):
            return {
                key: (
                    None
                    if (isinstance(value, str)
                        and value.strip().lower() == "null")
                    else value) for key, value in data.items()}
        return data


class DownloadQuery(BaseModel):
    download: bool = Field(
        False,
        description="Set to true to force the browser to download the file "
                    "instead of displaying it inline.")


class DateModel(BaseModel):
    earliest: str | None = Field(
        default=None,
        description="Earliest possible date (terminus post quem), "
                    "ISO 8601 formatted.",
        examples=["1450-01-01", "-0450-01-01"])
    latest: str | None = Field(
        default=None,
        description="Latest possible date (terminus ante quem), "
                    "ISO 8601 formatted. Equal to earliest for exact dates.",
        examples=["1455-12-31"])
    comment: str | None = Field(
        default=None,
        description="Optional textual note on date derivation, "
                    "uncertainty, or source.",
        examples=["15. cent."])


class TimeSpan(BaseModel):
    start: DateModel | None = Field(
        default=None,
        description="Beginning of the timespan.")
    end: DateModel | None = Field(
        default=None,
        description="End of the timespan.")


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


class ExtensionsType(str, Enum):
    JSON = 'json'
    TTL = 'ttl'
    XML = 'xml'
    NTRIPLES = 'nt'


class IiifVersion(str, Enum):
    V2 = "2"
    V3 = "3"


class MatchTypeEnum(str, Enum):
    EXACT_MATCH = "exactMatch"
    CLOSE_MATCH = "closeMatch"


class ExternalReferenceSystemModel(BaseModel):
    id: int
    name: str = Field(examples=["Wikidata", "Getty AAT"])
    description: str | None = Field(
        None,
        description="Description or scope note of the reference system.",
        examples=["A free and open knowledge base and common source of open "
                  "data providing persistent identifier and links to other "
                  "sources."])
    url: HttpUrl | None = Field(
        None,
        description="Direct link to the external entity.",
        examples=["https://www.wikidata.org/wiki/Q513532"])
    identifier: str | None = Field(
        None,
        description="The clean ID inside the external system "
                    "without resolver prefix.",
        examples=["Q513532"])
    match_type: MatchTypeEnum = Field(
        default=MatchTypeEnum.EXACT_MATCH,
        description="SKOS matching property.")
    system_url: HttpUrl | None = Field(
        None,
        description="Main homepage URL of the authority file provider.",
        examples=["https://www.wikidata.org"])


class ReferenceModel(BaseModel):
    id: int
    name: str
    class_name: str = Field(
        serialization_alias="class",
        description="The OpenAtlas entity class.",
        examples=["bibliography"])
    type: str | None = Field(
        description="Specific classification type.",
        examples=["book"])
    pages: str | None = Field(
        description="Page number, range, folio, or plate reference.",
        examples=["45-48", "fol. 12r", "Taf. 3, Abb. 2"])
    citation: str | None = Field(
        description="Full bibliographic citation text.",
        examples=[
            "Eichert, S. (2012). Frühmittelalterliche Strukturen im "
            "Ostalpenraum. Wien."])
