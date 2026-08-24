from enum import Enum


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
