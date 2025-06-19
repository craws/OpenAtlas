from __future__ import annotations

from typing import Any, Optional

from flask import g
from flask_babel import lazy_gettext as _

from config.model import model, view_class_mapping
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
        self.view = None
        self.alias_allowed = alias_allowed
        self.reference_system_allowed = reference_system_allowed
        self.reference_systems = reference_system_ids
        self.new_types_allowed = new_types_allowed
        self.icon = icon
        for item, classes in view_class_mapping.items():
            if name in classes:
                self.view = item
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


def get_table_headers() -> dict[str, list[str]]:
    headers = {
        'actor': ['name', 'class', 'begin', 'end', 'description'],
        'artifact': [
            'name', 'class', 'type', 'begin', 'end', 'description'],
        'entities': ['name', 'class', 'info'],
        'event': ['name', 'class', 'type', 'begin', 'end', 'description'],
        'external_reference': ['name', 'class', 'type', 'description'],
        'file': [
            'name', 'license', 'public', 'creator', 'license holder',
            'size', 'extension', 'description'],
        'member': ['member', 'function', 'first', 'last', 'description'],
        'member_of': [
            'member of', 'function', 'first', 'last', 'description'],
        'note': ['date', 'visibility', 'user', 'note'],
        'place': ['name', 'class', 'type', 'begin', 'end', 'description'],
        'relation': ['relation', 'actor', 'first', 'last', 'description'],
        'reference': ['name', 'class', 'type', 'description'],
        'reference_system': [
            'name', 'count', 'website URL', 'resolver URL', 'example ID',
            'default precision', 'description'],
        'source': ['name', 'type', 'content'],
        'source_translation': ['name', 'type', 'content'],
        'subs': ['name', 'count', 'info'],
        'text': ['text', 'type', 'content'],
        'type': ['name', 'description']}
    for view in ['actor', 'artifact', 'event', 'place']:
        for class_ in view_class_mapping[view]:
            headers[class_] = headers[view]
    return headers


def get_class_count() -> dict[str, int]:
    return db.get_class_count()


def get_class_view_mapping() -> dict['str', 'str']:
    mapping = {}
    for view, classes in view_class_mapping.items():
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
        item['label'] = item['label'] if 'label' in item else name
        item['required'] = item[
            'required'] if 'required' in item else False
    data['display'] = {} if 'display' not in data else data['display']
    data['display']['buttons'] = {} if 'buttons' not in data['display'] \
        else data['display']['buttons']
    data['relations'] = {} if 'relations' not in data else data[
        'relations']
    for name, relation in data['relations'].items():
        relation['class'] = relation['class'] \
            if isinstance(relation['class'], list) else [relation['class']]
        for item in ['inverse', 'label', 'mode', 'multiple', 'required']:
            if item not in relation:
                match item:
                    case 'label':
                        relation[item] = name
                    case 'inverse' | 'multiple' | 'required':
                        relation[item] = False
                    case 'mode':
                        relation[item] = None
        relation['selected'] = [] if relation['multiple'] else None
    return data
