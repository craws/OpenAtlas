from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Dict, List, Optional

from flask import g
from flask_babel import lazy_gettext as _

from openatlas.models.model import CidocClass
from openatlas.util.display import uc_first


class SystemClass:

    def __init__(self,
                 name: str,
                 cidoc_class: str,
                 label: Optional[str] = '',
                 standard_type: Optional[str] = None,
                 write_access: Optional[str] = 'contributor',
                 tabs: Optional[List[str]] = None,
                 form_fields: Optional[List[str]] = None) -> None:
        self.name = name
        self.label = uc_first(label)
        self.cidoc_class: CidocClass = g.cidoc_classes[cidoc_class]
        self.standard_type = standard_type
        self.write_access = write_access
        self.tabs = tabs if tabs else []
        self.form_fields = form_fields if form_fields else []
        self.table_headers = table_headers if table_headers else []
        self.view = None
        for item, classes in view_class_mapping.items():
            if name in classes:
                self.view = item


view_class_mapping = {
    'actor': ['person', 'group'],
    'event': ['activity', 'acquisition', 'move'],
    'file': ['file'],
    'artifact': ['artifact', 'find'],
    'place': ['feature', 'find', 'human_remains', 'place', 'stratigraphic_unit'],
    'reference': ['bibliography', 'edition', 'external_reference'],
    'reference_system': ['reference_system'],
    'source': ['source'],
    'type': ['administrative_unit', 'type'],
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

"""
missing standard_types:

Actor actor relation
Actor function
Involvement
Administrative unit
Historical place
External reference match
"""


def get_class_view_mapping() -> Dict['str', 'str']:
    mapping = {}
    for view, classes in view_class_mapping.items():
        for class_ in classes:
            mapping[class_] = view
    return mapping


def get_system_classes() -> Dict[str, SystemClass]:
    return {
        'acquisition': SystemClass(
            name='acquisition',
            cidoc_class='E8',
            label=_('acquisition'),
            standard_type='Event',
            tabs=[],
            form_fields=[]),
        'activity': SystemClass(
            name='activity',
            cidoc_class='E7',
            label=_('activity'),
            standard_type='Event',
            tabs=[],
            form_fields=[]),
        'actor_appellation': SystemClass(
            name='appellation',
            cidoc_class='E82'),
        'administrative_unit': SystemClass(
            name='administrative_unit',
            cidoc_class='E53',
            tabs=[],
            form_fields=[]),
        'appellation': SystemClass(
            name='appellation',
            cidoc_class='E41'),
        'artifact': SystemClass(
            name='artifact',
            cidoc_class='E22',
            label=_('artifact'),
            tabs=[],
            form_fields=[]),
        'bibliography': SystemClass(
            name='bibliography',
            cidoc_class='E31',
            label=_('bibliography'),
            standard_type='Bibliography',
            tabs=[],
            form_fields=[]),
        'edition': SystemClass(
            name='edition',
            cidoc_class='E31',
            label=_('edition'),
            standard_type='Edition',
            tabs=[],
            form_fields=[]),
        'external_reference': SystemClass(
            name='external_reference',
            cidoc_class='E31',
            label=_('external reference'),
            standard_type='External reference',
            write_access='manager',
            tabs=[],
            form_fields=[]),
        'feature': SystemClass(
            name='feature',
            cidoc_class='E18',
            label=_('feature'),
            standard_type='Feature',
            tabs=[],
            form_fields=[]),
        'file': SystemClass(
            name='file',
            cidoc_class='E31',
            label=_('file'),
            standard_type='License',
            tabs=[],
            form_fields=[]),
        'find': SystemClass(
            name='find',
            cidoc_class='E22',
            label=_('find'),
            tabs=[],
            form_fields=[]),
        'group': SystemClass(
            name='group',
            cidoc_class='E74',
            label=_('group'),
            tabs=[],
            form_fields=[]),
        'human_remains': SystemClass(
            name='human_remains',
            cidoc_class='E20',
            label=_('human remains'),
            standard_type='Human remains',
            tabs=[],
            form_fields=[]),
        'move': SystemClass(
            name='move',
            cidoc_class='E9',
            label=_('move'),
            standard_type='Event',
            tabs=[],
            form_fields=[]),
        'object_location': SystemClass(
            name='object_location',
            cidoc_class='E53'),
        'person': SystemClass(
            name='person',
            cidoc_class='E21',
            label=_('person'),
            tabs=[],
            form_fields=[]),
        'place': SystemClass(
            name='place',
            cidoc_class='E18',
            label=_('place'),
            standard_type='Place',
            tabs=[],
            form_fields=[]),
        'reference_system': SystemClass(
            name='reference_system',
            cidoc_class='E32',
            label=_('reference system'),
            tabs=[],
            form_fields=[]),
        'source': SystemClass(
            name='source',
            cidoc_class='E33',
            label=_('source'),
            standard_type='Source',
            tabs=['source', 'event', 'actor', 'place', 'feature', 'stratigraphic_unit', 'find',
                  'human_remains', 'reference', 'node', 'object'],
            form_fields=[]),
        'stratigraphic_unit': SystemClass(
            name='stratigraphic_unit',
            cidoc_class='E18',
            label=_('stratigraphic unit'),
            standard_type='Stratigraphic unit',
            tabs=[],
            form_fields=[]),
        'translation': SystemClass(
            name='translation',
            cidoc_class='E33',
            label=_('translation'),
            tabs=[],
            form_fields=[]),
        'type': SystemClass(
            name='type',
            cidoc_class='E55',
            label=_('type'),
            write_access='editor',
            tabs=[],
            form_fields=[])}
