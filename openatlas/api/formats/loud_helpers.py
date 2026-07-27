from typing import Any
from openatlas import app

LANGUAGES: dict[str, dict[str, Any]] = {
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

UNIT_MAP = {
    'B': 'bytes',
    'KB': 'kilobytes',
    'MB': 'megabytes',
    'GB': 'gigabytes',
    'TB': 'terabytes'}

TYPE_OVERWRITES = {
    'file': 'DigitalObject',
    'human_remains': 'BiologicalObject',
    'place': 'Site',
    'feature': 'HumanMadeFeature',
    'stratigraphic_unit':
        'https://www.cidoc-crm.org/extensions/crmarchaeo/'
        'A8_Stratigraphic_Unit'}


def aat_type(id_: str, label: str) -> dict[str, str]:
    return {
        'id': f'https://vocab.getty.edu/aat/{id_}',
        'type': 'Type',
        '_label': label}


ARCHAEOLOGY_AAT: dict[str, dict[str, str]] = {
    'artifact': aat_type('300117127', 'artifacts'),
    'human_remains': aat_type('300379896', 'human remains')}

MIME_CLASSIFICATIONS: dict[str, list[dict[str, str]]] = {
    'image/': [aat_type('300215302', 'Digital image')],
    'application/pdf': [aat_type('300424602', 'Digital documents')],
    'model/': [
        aat_type('300266011', 'Digital File Format'), {
            'id': 'https://www.wikidata.org/wiki/Q3859833',
            'type': 'Type',
            '_label': '3D Model'}]}

BIBLIOGRAPHY_AAT: dict[str, dict[str, str]] = {
    'bibliography': aat_type('300026497', 'bibliography'),
    'edition': aat_type('300121294', 'edition')}


def get_language() -> dict[str, Any]:
    code = app.config.get('ARCHE_METADATA', {}).get('language', 'en')
    return LANGUAGES.get(code, LANGUAGES['en'])


def category_aat(id_: str, label: str) -> dict[str, Any]:
    return aat_type(id_, label) \
        | {'classified_as': [aat_type('300137954', 'documents (by form)')]}


def primary_name(
        content: str,
        label: str | None = None,
        id_: str | None = None) -> dict[str, Any]:
    name: dict[str, Any] = {
        'type': 'Name',
        '_label': label or content,
        'content': content,
        'classified_as': [aat_type('300404670', 'primary name')],
        'language': [get_language()]}
    if id_:
        name = {'id': id_} | name
    return name
