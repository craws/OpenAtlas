from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator
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
