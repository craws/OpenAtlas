from typing import Any, Final

from openatlas import app
from openatlas.models.entity import Entity

LANGUAGES: Final[dict[str, dict[str, Any]]] = {
    'en': {
        'id': 'https://vocab.getty.edu/aat/300388277',
        'type': 'Language',
        '_label': 'English'},
    'de': {
        'id': 'https://vocab.getty.edu/aat/300388344',
        'type': 'Language',
        '_label': 'German'},
    'fr': {
        'id': 'https://vocab.getty.edu/aat/300388306',
        'type': 'Language',
        '_label': 'French'},
    'it': {
        'id': 'https://vocab.getty.edu/aat/300388474',
        'type': 'Language',
        '_label': 'Italian'},
    'es': {
        'id': 'https://vocab.getty.edu/aat/300389311',
        'type': 'Language',
        '_label': 'Spanish'},
    'sr': {
        'id': 'https://vocab.getty.edu/aat/300389248',
        'type': 'Language',
        '_label': 'Serbian'},
    'sl': {
        'id': 'https://vocab.getty.edu/aat/300389291',
        'type': 'Language',
        '_label': 'Slovenian'},
    'cs': {
        'id': 'https://vocab.getty.edu/aat/300388191',
        'type': 'Language',
        '_label': 'Czech'},
    'sk': {
        'id': 'https://vocab.getty.edu/aat/300389290',
        'type': 'Language',
        '_label': 'Slovak'}}

UNIT_MAP: Final[dict[str, str]] = {
    'B': 'bytes',
    'KB': 'kilobytes',
    'MB': 'megabytes',
    'GB': 'gigabytes',
    'TB': 'terabytes'}

# OpenAtlas system class -> Linked Art class
LA_TYPES: Final[dict[str, str]] = {
    'acquisition': 'Activity',
    'activity': 'Activity',
    'modification': 'Activity',
    'move': 'Activity',
    'production': 'Activity',
    'administrative_unit': 'Place',
    'object_location': 'Place',
    'place': 'HumanMadeObject',
    'artifact': 'HumanMadeObject',
    'feature': 'HumanMadeObject',
    'human_remains': 'HumanMadeObject',
    'stratigraphic_unit': 'HumanMadeObject',
    'file': 'DigitalObject',
    'person': 'Person',
    'group': 'Group',
    'bibliography': 'LinguisticObject',
    'edition': 'LinguisticObject',
    'external_reference': 'LinguisticObject',
    'reference_system': 'LinguisticObject',
    'source': 'LinguisticObject',
    'text': 'LinguisticObject',
    'type': 'Type',
    'type_tools': 'Type'}

ACTORS: Final[set[str]] = {'Person', 'Group'}
DIMENSION_ROOTS: Final[set[str]] = {
    'HumanMadeObject', 'DigitalObject', 'LinguisticObject', 'Set'}


def aat_type(id_: str, label: str) -> dict[str, str]:
    return {
        'id': f'https://vocab.getty.edu/aat/{id_}',
        'type': 'Type',
        '_label': label}


def crm_type(code: str, label: str) -> dict[str, str]:
    return {
        'id': f"http://www.cidoc-crm.org/cidoc-crm/"
              f"{code}_{label.replace(' ', '_')}",
        'type': 'Type',
        '_label': label}


ARCHAEOLOGY_AAT: Final[dict[str, dict[str, str]]] = {
    'artifact': aat_type('300117127', 'artifacts'),
    'human_remains': aat_type('300379896', 'human remains')}

BIBLIOGRAPHY_AAT: Final[dict[str, dict[str, str]]] = {
    'bibliography': aat_type('300026497', 'bibliography'),
    'edition': aat_type('300121294', 'edition')}

# Classes where the Linked Art class alone is too coarse
CLASS_TYPES: Final[dict[str, list[dict[str, str]]]] = {
    'artifact': [ARCHAEOLOGY_AAT['artifact']],
    'human_remains': [ARCHAEOLOGY_AAT['human_remains']],
    'place': [crm_type('E18', 'Physical Thing')],
    'feature': [crm_type('E25', 'Man-Made Feature')],
    'stratigraphic_unit': [{
        'id': 'https://www.cidoc-crm.org/extensions/crmarchaeo/'
              'A8_Stratigraphic_Unit',
        'type': 'Type',
        '_label': 'Stratigraphic Unit'}],
    'acquisition': [crm_type('E8', 'Acquisition')],
    'modification': [crm_type('E11', 'Modification')],
    'move': [crm_type('E9', 'Move')],
    'production': [crm_type('E12', 'Production')],
    'bibliography': [BIBLIOGRAPHY_AAT['bibliography']],
    'edition': [BIBLIOGRAPHY_AAT['edition']],
    'external_reference': [aat_type('300264578', 'web page')],
    'reference_system': [crm_type('E32', 'Authority Document')]}

MIME_CLASSIFICATIONS: Final[dict[str, list[dict[str, str]]]] = {
    'image/': [aat_type('300215302', 'Digital image')],
    'application/pdf': [aat_type('300424602', 'Digital documents')],
    'model/': [
        aat_type('300266011', 'Digital File Format'), {
            'id': 'https://www.wikidata.org/wiki/Q3859833',
            'type': 'Type',
            '_label': '3D Model'}]}


def la_type(entity: Entity) -> str:
    return LA_TYPES.get(entity.class_.name, 'LinguisticObject')


def get_language() -> dict[str, Any]:
    code = app.config.get('ARCHE_METADATA', {}).get('language', 'en')
    return LANGUAGES.get(code, LANGUAGES['en'])


def category_aat(id_: str, label: str) -> dict[str, Any]:
    return aat_type(id_, label) \
        | {'classified_as': [aat_type('300137954', 'documents (by form)')]}


def primary_name(content: str, label: str | None = None) -> dict[str, Any]:
    return {
        'type': 'Name',
        '_label': label or content,
        'content': content,
        'classified_as': [aat_type('300404670', 'primary name')],
        'language': [get_language()]}


def alias_name(content: str) -> dict[str, Any]:
    return {
        'type': 'Name',
        '_label': content,
        'content': content,
        'language': [get_language()]}


def identifier(
        content: str,
        label: str,
        classified_as: dict[str, Any] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        'type': 'Identifier',
        '_label': label,
        'content': content}
    if classified_as:
        result['classified_as'] = [classified_as]
    return result


def unique_identifier(uri: str) -> dict[str, Any]:
    return identifier(
        uri,
        'Unique Identifier',
        aat_type('300404012', 'unique identifier'))


def statement(
        content: str,
        label: str,
        classified_as: list[dict[str, Any]] | None = None,
        identified_by: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        'type': 'LinguisticObject',
        '_label': label,
        'content': content,
        'language': [get_language()]}
    if classified_as:
        result['classified_as'] = classified_as
    if identified_by:
        result['identified_by'] = identified_by
    return result
