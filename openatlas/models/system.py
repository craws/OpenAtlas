from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Dict, List, Optional

from flask import g

from openatlas.models.model import CidocClass


class SystemClass:

    def __init__(self,
                 name: str,
                 cidoc_class: str,
                 write_access: Optional[str] = 'contributor',
                 tabs: Optional[List[str]] = None,
                 form_fields: Optional[List[str]] = None) -> None:
        self.name = name
        self.cidoc_class: CidocClass = g.cidoc_classes[cidoc_class]
        self.write_access = write_access
        self.view = view_class_mapping[name] if name in view_class_mapping else None
        self.tabs = tabs if tabs else []
        self.form_fields = form_fields if form_fields else []
        self.table_headers = table_headers if table_headers else []


view_class_mapping = {
    'actor': ['group', 'person'],
    'event': ['acquisition', 'activity', 'move'],
    'file': ['file'],
    'artifact': ['artifact'],
    'place': ['feature', 'find', 'human_remains', 'place', 'stratigraphic_unit'],
    'reference': ['bibliography', 'edition', 'external_reference'],
    'reference_system': ['reference_system'],
    'source': ['source'],
    'type': ['location', 'type'],
    'translation': ['translation']}

table_headers = {
    'actor': ['name', 'class', 'begin', 'end', 'description'],
    'artifact': ['name', 'type', 'begin', 'end', 'description'],
    'entities': ['name', 'class', 'info'],
    'event': ['name', 'class', 'type', 'begin', 'end', 'description'],
    'feature': ['name', 'type', 'begin', 'end', 'description'],
    'find': ['name', 'type', 'begin', 'end', 'description'],
    'file': ['name', 'license', 'size', 'extension', 'description'],
    'group': ['name', 'class', 'begin', 'end', 'description'],
    'human_remains': ['name', 'type', 'begin', 'end', 'description'],
    'member': ['member', 'function', 'first', 'last', 'description'],
    'member_of': ['member of', 'function', 'first', 'last', 'description'],
    'node': ['name', 'description'],
    'object': ['name', 'type', 'description'],
    'person': ['name', 'class', 'begin', 'end', 'description'],
    'place': ['name', 'type', 'begin', 'end', 'description'],
    'relation': ['relation', 'actor', 'first', 'last', 'description'],
    'reference': ['name', 'class', 'type', 'description'],
    'reference_system': ['name', 'count', 'website URL', 'resolver URL', 'example ID',
                         'default precision', 'description'],
    'source': ['name', 'type', 'description'],
    'stratigraphic_unit': ['name', 'type', 'begin', 'end', 'description'],
    'text': ['text', 'type', 'content']}


def get_class_view_mapping() -> Dict['str', 'str']:
    mapping = {}
    for view, classes in view_class_mapping.items():
        for class_ in classes:
            mapping[class_] = view
    return mapping


system_classes: Dict[str, SystemClass] = {
    'acquisition': SystemClass(
        name='acquisition',
        cidoc_class='E8',
        tabs=[],
        form_fields=[]),
    'activity': SystemClass(
        name='activity',
        cidoc_class='E7',
        tabs=[],
        form_fields=[]),
    'actor_appellation': SystemClass(
        name='appellation',
        cidoc_class='E82'),
    'appellation': SystemClass(
        name='appellation',
        cidoc_class='E41'),
    'artifact': SystemClass(
        name='type',
        cidoc_class='E22',
        tabs=[],
        form_fields=[]),
    'bibliography': SystemClass(
        name='bibliography',
        cidoc_class='E31',
        tabs=[],
        form_fields=[]),
    'edition': SystemClass(
        name='edition',
        cidoc_class='E31',
        tabs=[],
        form_fields=[]),
    'external_reference': SystemClass(
        name='external_reference',
        cidoc_class='E31',
        tabs=[],
        form_fields=[]),
    'feature': SystemClass(
        name='feature',
        cidoc_class='E18',
        tabs=[],
        form_fields=[]),
    'file': SystemClass(
        name='file',
        cidoc_class='E31',
        tabs=[],
        form_fields=[]),
    'find': SystemClass(
        name='find',
        cidoc_class='E22',
        tabs=[],
        form_fields=[]),
    'group': SystemClass(
        name='type',
        cidoc_class='E74',
        tabs=[],
        form_fields=[]),
    'human_remains': SystemClass(
        name='human_remains',
        cidoc_class='E20',
        tabs=[],
        form_fields=[]),
    'information_carrier': SystemClass(
        name='information_carrier',
        cidoc_class='E84',
        tabs=[],
        form_fields=[]),
    'legal_body': SystemClass(
        name='legal_body',
        cidoc_class='E40',
        tabs=[],
        form_fields=[]),
    'location': SystemClass(
        name='location',
        cidoc_class='E53',
        tabs=[],
        form_fields=[]),
    'move': SystemClass(
        name='move',
        cidoc_class='E9',
        tabs=[],
        form_fields=[]),
    'object_location': SystemClass(
        name='object_location',
        cidoc_class='E53'),
    'person': SystemClass(
        name='person',
        cidoc_class='E21',
        tabs=[],
        form_fields=[]),
    'place': SystemClass(
        name='place',
        cidoc_class='E18',
        tabs=[],
        form_fields=[]),
    'reference_system': SystemClass(
        name='reference_system',
        cidoc_class='E32',
        tabs=[],
        form_fields=[]),
    'source': SystemClass(
        name='source',
        cidoc_class='E33',
        tabs=['source', 'event', 'actor', 'place', 'feature', 'stratigraphic_unit', 'find',
              'human_remains', 'reference', 'node', 'object'],
        form_fields=[]),
    'stratigraphic_unit': SystemClass(
        name='stratigraphic_unit ',
        cidoc_class='E18',
        tabs=[],
        form_fields=[]),
    'translation': SystemClass(
        name='translation',
        cidoc_class='E33',
        tabs=[],
        form_fields=[]),
    'type': SystemClass(
        name='type',
        cidoc_class='E55',
        write_access='editor',
        tabs=[],
        form_fields=[])}
