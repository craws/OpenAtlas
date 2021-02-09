from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Dict, List, Optional

from flask import g

from openatlas.models.model import CidocClass


class SystemClass:

    def __init__(self,
                 name: str,
                 cidoc_class: str,
                 view_class: Optional[str] = None,
                 write_access: Optional[str] = 'contributor',
                 tabs: Optional[List[str]] = None,
                 form_fields: Optional[List[str]] = None,
                 table_headers: Optional[List[str]] = None) -> None:
        self.name = name
        self.cidoc_class: CidocClass = g.classes[cidoc_class]
        self.write_access = write_access
        self.view_class = view_class
        self.tabs = tabs if tabs else []
        self.form_fields = form_fields if form_fields else []
        self.table_headers = table_headers if table_headers else []


instances: Dict[str, SystemClass] = {
    'acquisition ': SystemClass(
        name='acquisition',
        cidoc_class='E8',
        view_class='event',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'activity': SystemClass(
        name='activity',
        cidoc_class='E7',
        view_class='event',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'actor_appellation': SystemClass(
        name='appellation',
        cidoc_class='E82'),
    'appellation': SystemClass(
        name='appellation',
        cidoc_class='E41'),
    'artificial_object': SystemClass(
        name='type',
        cidoc_class='E22',
        view_class='object',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'bibliography': SystemClass(
        name='bibliography',
        cidoc_class='E31',
        view_class='reference',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'edition': SystemClass(
        name='edition',
        cidoc_class='E31',
        view_class='reference',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'external_reference': SystemClass(
        name='external_reference',
        cidoc_class='E31',
        view_class='reference',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'feature': SystemClass(
        name='feature',
        cidoc_class='E18',
        view_class='place',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'file': SystemClass(
        name='file',
        cidoc_class='E31',
        view_class='file',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'find': SystemClass(
        name='find',
        cidoc_class='E22',
        view_class='place',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'group': SystemClass(
        name='type',
        cidoc_class='E74',
        view_class='actor',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'human_remains': SystemClass(
        name='human_remains',
        cidoc_class='E20',
        view_class='place',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'information_carrier': SystemClass(
        name='information_carrier',
        cidoc_class='E84',
        view_class='object',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'legal_body': SystemClass(
        name='legal_body',
        cidoc_class='E40',
        view_class='actor',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'location': SystemClass(
        name='location',
        cidoc_class='E53',
        view_class='type',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'move': SystemClass(
        name='move',
        cidoc_class='E9',
        view_class='event',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'object_location': SystemClass(
        name='object_location',
        cidoc_class='E53'),
    'person': SystemClass(
        name='person',
        cidoc_class='E21',
        view_class='actor',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'place': SystemClass(
        name='place',
        cidoc_class='E18',
        view_class='place',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'reference_system': SystemClass(
        name='reference_system',
        cidoc_class='E32',
        view_class='reference_system',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'source': SystemClass(
        name='source',
        cidoc_class='E33',
        view_class='source',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'stratigraphic_unit': SystemClass(
        name='stratigraphic_unit ',
        cidoc_class='E18',
        view_class='place',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'translation': SystemClass(
        name='translation',
        cidoc_class='E33',
        view_class='translation',
        tabs=[],
        form_fields=[],
        table_headers=[]),
    'type': SystemClass(
        name='type',
        cidoc_class='E55',
        view_class='type',
        write_access='editor',
        tabs=[],
        form_fields=[],
        table_headers=[])}
