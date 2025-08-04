from __future__ import annotations

from typing import Any, Optional

from flask import g
from flask_babel import lazy_gettext as _

from config.model.model import model
from config.model.class_groups import class_groups
from openatlas.database import openatlas_class as db


class OpenatlasClass:
    # Needed class label translations
    _('acquisition')
    _('actor relation')
    _('actor function')
    _('administrative unit')
    _('appellation')
    _('bibliography')
    _('creation')
    _('external reference')
    _('feature')
    _('information carrier')  # Not an OpenAtlas class, used at source display
    _('involvement')
    _('modification')
    _('move')
    _('production')
    _('object location')
    _('source translation')
    _('type tools')

    def __init__(
            self,
            name: str,
            cidoc_class: str | None,
            hierarchies: list[int],
            alias_allowed: bool,
            reference_system_allowed: bool,
            reference_system_ids: list[int],
            new_types_allowed: bool,
            standard_type_id: int | None,
            color: str | None,
            write_access: str | None,
            icon: str | None,
            attributes: dict[str, Any],
            relations: dict[str, Any],
            display: dict[str, Any]) -> None:
        self.name = name
        label = _(name.replace('_', ' '))
        self.label = str(label)[0].upper() + str(label)[1:]
        self.cidoc_class = g.cidoc_classes[cidoc_class] \
            if cidoc_class else None
        self.hierarchies = hierarchies
        self.standard_type_id = standard_type_id
        self.network_color = color
        self.write_access = write_access or 'contributor'
        self.group = None
        self.alias_allowed = alias_allowed
        self.reference_system_allowed = reference_system_allowed
        self.reference_systems = reference_system_ids
        self.new_types_allowed = new_types_allowed
        self.icon = icon
        for item, classes in class_groups.items():
            if name in classes:
                self.group = item
        self.attributes = attributes
        self.relations = relations
        self.display = display

    def get_tooltip(self) -> Optional[str]:
        tooltips = {
            'E5': _('events not performed by actors, e.g. a natural disaster'),
            'E7': _('the most common, e.g. a battle, a meeting or a wedding'),
            'E8': _('mapping a change of property'),
            'E9': _('movement of artifacts or persons'),
            'E11': _('modification of artifacts'),
            'E12': _('creation of artifacts'),
            'E65': _('creation of documents (files)')}
        if self.cidoc_class.code in tooltips:
            return tooltips[self.cidoc_class.code]
        return None


def get_class_count() -> dict[str, int]:
    return db.get_class_count()


def get_class_view_mapping() -> dict['str', 'str']:
    mapping = {}
    for view, classes in class_groups.items():
        for class_ in classes:
            mapping[class_] = view
    return mapping


def get_classes() -> dict[str, OpenatlasClass]:
    classes = {}
    for row in db.get_classes():
        model_ = get_model(row['name'])
        classes[row['name']] = OpenatlasClass(
            name=row['name'],
            cidoc_class=row['cidoc_class_code'],
            standard_type_id=row['standard_type_id'],
            alias_allowed=row['alias_allowed'],
            reference_system_allowed=row['reference_system_allowed'],
            reference_system_ids=row['system_ids']
            if row['system_ids'] else [],
            new_types_allowed=row['new_types_allowed'],
            write_access=row['write_access_group_name'],
            color=row['layout_color'],
            hierarchies=row['hierarchies'],
            icon=row['layout_icon'],
            attributes=model_['attributes'],
            relations=model_['relations'],
            display=model_['display'])
    return classes


def get_model(class_name: str) -> dict[str, Any]:
    data: dict[str, Any] = model[class_name]
    for name, item in data['attributes'].items():
        item['label'] = item.get('label', name)
        item['required'] = item.get('required', False)
    data['display'] = data.get('display', {})
    data['display']['buttons'] = data['display'].get('buttons', {})
    data['display']['tabs'] = data['display'].get('tabs', {})
    for tab in data['display']['tabs'].values():
        tab['columns'] = tab.get('columns', None)
        tab['additional_columns'] = tab.get('additional_columns', [])
        tab['mode'] = tab.get('mode', None)
    data['relations'] = data.get('relations', {})
    for name, relation in data['relations'].items():
        relation['class'] = relation['class'] \
            if isinstance(relation['class'], list) else [relation['class']]
        relation['inverse'] = relation.get('inverse', False)
        relation['multiple'] = relation.get('multiple', False)
        relation['required'] = relation.get('required', False)
        relation['label'] = relation.get('label', name)
        relation['mode'] = relation.get('mode', 'tab')
        relation['selected'] = [] if relation['multiple'] else None
        relation['tooltip'] = relation.get('tooltip', None)
    return data
