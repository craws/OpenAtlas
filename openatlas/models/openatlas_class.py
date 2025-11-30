from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from flask import g
from flask_babel import lazy_gettext as _

from config.model.class_groups import class_groups
from config.model.model import model
from openatlas.database import openatlas_class as db


@dataclass
class OpenatlasClass:
    name: str
    cidoc_class: str
    hierarchies: list[int]
    reference_systems: list[int]
    new_types_allowed: bool
    standard_type_id: int | None
    write_access: str
    attributes: dict[str, Any]
    relations: dict[str, Any]
    display: dict[str, Any]
    extra: dict[str, Any]

    def __post_init__(self) -> None:
        self.group = {}
        for data in g.class_groups.values():
            if self.name in data['classes']:
                self.group = data
        self.label = _(self.name.replace('_', ' '))
        self.label = str(self.label)[0].upper() + str(self.label)[1:]


@dataclass
class Relation:
    name: str
    property: str
    classes: list[str]
    inverse: bool = False
    multiple: bool = False
    required: bool = False
    label: str = ''
    mode: str = 'tab'
    add_dynamic: bool = False
    tooltip: str | None = None
    additional_fields: list[str] = field(default_factory=list)
    type: str | None = None
    reverse_relation: Relation | None = None
    tab: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.label = self.label or _(self.name.replace('_', ' '))
        if self.mode == 'tab':
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
        model_ = get_model(row['name'])
        relations = {}
        for name_, relation in model_['relations'].items():
            relations[name_] = Relation(name_, **relation)
        classes[row['name']] = OpenatlasClass(
            name=row['name'],
            cidoc_class=g.cidoc_classes[row['cidoc_class_code']],
            standard_type_id=row['standard_type_id'],
            reference_systems=row['system_ids']
            if row['system_ids'] else [],
            new_types_allowed=row['new_types_allowed'],
            write_access=row['write_access_group_name'],
            hierarchies=row['hierarchies'],
            attributes=model_['attributes'],
            relations=relations,
            display=model_['display'],
            extra=model_['extra'])
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
                if class_.name == 'place' and 'object_location' \
                        in relation2.classes \
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


def get_db_relations() -> list[dict[str, Any]]:
    return db.get_db_relations()


def get_model_relations() -> dict[str, Any]:
    relations: dict[str, Any] = {}
    for name, data in model.items():
        for relation in data['relations'].values():
            for range_ in relation['classes']:
                domain = range_ if relation.get('inverse') else name
                range_ = name if relation.get('inverse') else range_
                relations[domain] = relations.get(domain, {})
                relations[domain][range_] = relations[domain].get(range_, {})
                if relation['property'] not in relations[domain][range_]:
                    relations[domain][range_][relation['property']] = 1
                else:
                    relations[domain][range_][relation['property']] += 1
    return relations
