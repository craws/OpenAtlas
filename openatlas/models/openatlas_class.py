from __future__ import annotations

from typing import Any

from flask import g
from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups
from config.model.model import model
from openatlas.database import openatlas_class as db


class OpenatlasClass:
    def __init__(
            self,
            name: str,
            cidoc_class: str | None,
            hierarchies: list[int],
            reference_system_ids: list[int],
            new_types_allowed: bool,
            standard_type_id: int | None,
            color: str | None,
            write_access: str | None,
            icon: str | None,
            model_: dict[str, Any]) -> None:
        self.name = name
        self.cidoc_class = g.cidoc_classes[cidoc_class] \
            if cidoc_class else None
        self.hierarchies = hierarchies
        self.standard_type_id = standard_type_id
        self.network_color = color
        self.write_access = write_access or 'contributor'
        self.reference_systems = reference_system_ids
        self.new_types_allowed = new_types_allowed
        self.icon = icon
        self.group = {}
        for data in g.class_groups.values():
            if name in data['classes']:
                self.group = data
        self.label = model_['label']
        self.attributes = model_['attributes']
        self.relations = model_['relations']
        self.display = model_['display']
        self.extra = model_['extra']


def get_class_count() -> dict[str, int]:
    return db.get_class_count()


def get_classes() -> dict[str, OpenatlasClass]:
    g.class_groups = class_groups
    classes = {}
    for row in db.get_classes():
        if row['name'] in model:  # Todo: remove condition after new classes
            classes[row['name']] = OpenatlasClass(
                name=row['name'],
                model_=get_model(row['name']),
                cidoc_class=row['cidoc_class_code'],
                standard_type_id=row['standard_type_id'],
                reference_system_ids=row['system_ids']
                if row['system_ids'] else [],
                new_types_allowed=row['new_types_allowed'],
                write_access=row['write_access_group_name'],
                color=row['layout_color'],
                hierarchies=row['hierarchies'],
                icon=row['layout_icon'])
    return classes


def get_model(class_name: str) -> dict[str, Any]:
    data: dict[str, Any] = model[class_name]
    data['label'] = data.get('label', _(class_name))
    for name, item in data['attributes'].items():
        item['label'] = item.get('label', _(name))
        item['required'] = item.get('required', False)
    data['display'] = data.get('display', {})
    data['display']['tooltip'] = data['display'].get('tooltip')
    data['display']['additional_tabs'] = \
        data['display'].get('additional_tabs', {})
    data['display']['buttons'] = data['display'].get('buttons', {})
    data['display']['form_buttons'] = data['display'].get('form_buttons', [])
    data['display']['additional_information'] = \
        data['display'].get('additional_information', {})
    for name, item in data['display']['additional_information'].items():
        item['label'] = item.get('label', _(name))
    data['extra'] = data.get('extra', [])
    data['relations'] = data.get('relations', {})
    for name, relation in data['relations'].items():
        relation['name'] = name
        relation['classes'] = relation['classes'] \
            if isinstance(relation['classes'], list) \
            else [relation['classes']]
        relation['inverse'] = relation.get('inverse', False)
        relation['multiple'] = relation.get('multiple', False)
        relation['required'] = relation.get('required', False)
        relation['label'] = relation.get('label', _(name.replace('_', ' ')))
        relation['mode'] = relation.get('mode', 'tab')
        relation['add_dynamic'] = relation.get('add_dynamic', False)
        relation['selected'] = [] if relation['multiple'] else None
        relation['tooltip'] = relation.get('tooltip')
        relation['additional_fields'] = relation.get('additional_fields', [])
        if relation['mode'] == 'tab':
            relation['tab'] = relation.get('tab', {})
            relation['tab']['additional_columns'] = \
                relation['tab'].get('additional_columns', [])
            relation['tab']['buttons'] = relation['tab'].get('buttons', [])
            relation['tab']['columns'] = relation['tab'].get('columns')
            relation['tab']['tooltip'] = relation['tab'].get('tooltip')
    return data


def get_reverse_relation(
        class_: OpenatlasClass,
        relation: dict[str, Any],
        reverse_class: OpenatlasClass) -> dict[str, Any] | None:
    for reverse_relation in reverse_class.relations.values():
        if class_.name in reverse_relation['classes'] \
                and relation['property'] == reverse_relation['property'] \
                and relation['inverse'] != reverse_relation['inverse']:
            return reverse_relation
    return None
