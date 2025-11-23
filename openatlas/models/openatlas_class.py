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
            write_access: str | None,
            model_: dict[str, Any]) -> None:
        self.name = name
        self.cidoc_class = g.cidoc_classes[cidoc_class] \
            if cidoc_class else None
        self.hierarchies = hierarchies
        self.standard_type_id = standard_type_id
        self.write_access = write_access or 'contributor'
        self.reference_systems = reference_system_ids
        self.new_types_allowed = new_types_allowed
        self.group = {}
        for data in g.class_groups.values():
            if name in data['classes']:
                self.group = data
        label = model_.get('label', _(name.replace('_', ' ')))
        self.label = str(label)[0].upper() + str(label)[1:]
        self.attributes = model_['attributes']
        self.relations = {}
        for name_, relation in model_['relations'].items():
            self.relations[name_] = Relation(name_, relation)
        self.display = model_['display']
        self.extra = model_['extra']


class Relation:
    def __init__(self, name: str, data: dict[str, Any]) -> None:
        self.name = name
        self.property = data['property']
        self.classes = data['classes'] if isinstance(data['classes'], list) \
            else [data['classes']]
        self.inverse = data.get('inverse', False)
        self.multiple = data.get('multiple', False)
        self.required = data.get('required', False)
        self.label = data.get('label', _(self.name.replace('_', ' ')))
        self.mode = data.get('mode', 'tab')
        self.add_dynamic = data.get('add_dynamic', False)
        self.tooltip = data.get('tooltip')
        self.additional_fields = data.get('additional_fields', [])
        self.via_location = data.get('via_location', False)
        self.type = data.get('type')
        self.reverse_relation: Relation | None = None
        if self.mode == 'tab':
            self.tab = data.get('tab', {})
            self.tab['additional_columns'] = \
                self.tab.get('additional_columns', [])
            self.tab['buttons'] = self.tab.get('buttons', [])
            self.tab['columns'] = self.tab.get('columns')
            self.tab['tooltip'] = self.tab.get('tooltip')


def get_class_count() -> dict[str, int]:
    return db.get_class_count()


def get_classes() -> dict[str, OpenatlasClass]:
    g.class_groups = class_groups
    classes = {}
    for row in db.get_classes():
        classes[row['name']] = OpenatlasClass(
            name=row['name'],
            model_=get_model(row['name']),
            cidoc_class=row['cidoc_class_code'],
            standard_type_id=row['standard_type_id'],
            reference_system_ids=row['system_ids']
            if row['system_ids'] else [],
            new_types_allowed=row['new_types_allowed'],
            write_access=row['write_access_group_name'],
            hierarchies=row['hierarchies'])
    for class_ in classes.values():
        for relation in class_.relations.values():
            if not relation.classes:
                continue
            related_class = classes[
                relation.classes[0].replace('object_location', 'place')]
            for relation2 in related_class.relations.values():
                if class_.name in relation2.classes \
                        and relation.property == relation2.property \
                        and relation.inverse != relation2.inverse:
                    relation.reverse_relation = relation2
                    break
    return classes


def get_model(class_name: str) -> dict[str, Any]:
    data: dict[str, Any] = model[class_name]
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
    return data
