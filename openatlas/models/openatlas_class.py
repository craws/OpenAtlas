from __future__ import annotations

from typing import Optional

from flask import g
from flask_babel import lazy_gettext as _

from openatlas.database.openatlas_class import OpenAtlasClass as Db

view_class_mapping = {
    'actor': ['person', 'group'],
    'event': [
        'activity', 'acquisition', 'creation', 'event', 'move', 'production'],
    'file': ['file'],
    'artifact': ['artifact', 'human_remains'],
    'place': ['feature', 'place', 'stratigraphic_unit'],
    'reference': ['bibliography', 'edition', 'external_reference'],
    'reference_system': ['reference_system'],
    'source': ['source'],
    'type': ['administrative_unit', 'type'],
    'source_translation': ['source_translation']}


class OpenatlasClass:

    # Needed class label translations
    _('acquisition')
    _('actor relation')
    _('actor function')
    _('appellation')
    _('bibliography')
    _('external reference')
    _('source translation')

    def __init__(
            self,
            name: str,
            cidoc_class: str,
            hierarchies: list[int],
            alias_allowed: bool,
            reference_system_allowed: bool,
            reference_system_ids: list[int],
            new_types_allowed: bool,
            standard_type_id: Optional[int] = None,
            color: Optional[str] = None,
            write_access: str = 'contributor',
            icon: Optional[str] = None) -> None:
        self.name = name
        label = _(name.replace('_', ' '))
        self.label = str(label)[0].upper() + str(label)[1:]
        self.cidoc_class = g.cidoc_classes[cidoc_class] \
            if cidoc_class else None
        self.hierarchies = hierarchies
        self.standard_type_id = standard_type_id
        self.network_color = color
        self.write_access = write_access
        self.view = None
        self.alias_allowed = alias_allowed
        self.reference_system_allowed = reference_system_allowed
        self.reference_systems = reference_system_ids
        self.new_types_allowed = new_types_allowed
        self.icon = icon
        for item, classes in view_class_mapping.items():
            if name in classes:
                self.view = item

    def get_tooltip(self):
        tooltips = {
            'E5': _('events not performed by actors, e.g. a natural disaster'),
            'E7': _('the most common, e.g. a battle, a meeting or a wedding'),
            'E8': _('mapping a change of property'),
            'E9': _('movement of artifacts or persons'),
            'E12': _('creation of artifacts'),
            'E65': _('creation of documents (files)')}
        if self.cidoc_class.code in tooltips:
            return tooltips[self.cidoc_class.code]
        return None

    @staticmethod
    def get_class_count() -> dict[str, int]:
        return Db.get_class_count()

    @staticmethod
    def get_all() -> dict[str, OpenatlasClass]:
        classes = {}
        for row in Db.get_classes():
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
                icon=row['layout_icon'])
        return classes

    @staticmethod
    def get_table_headers() -> dict[str, list[str]]:
        headers = {
            'actor': ['name', 'class', 'begin', 'end', 'description'],
            'artifact': [
                'name', 'class', 'type', 'begin', 'end', 'description'],
            'entities': ['name', 'class', 'info'],
            'event': ['name', 'class', 'type', 'begin', 'end', 'description'],
            'file': ['name', 'license', 'size', 'extension', 'description'],
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
            'source': ['name', 'type', 'description'],
            'subs': ['name', 'count', 'info'],
            'text': ['text', 'type', 'content'],
            'type': ['name', 'description']}
        for view in ['actor', 'artifact', 'event', 'place']:
            for class_ in view_class_mapping[view]:
                headers[class_] = headers[view]
        return headers

    @staticmethod
    def get_class_view_mapping() -> dict['str', 'str']:
        mapping = {}
        for view, classes in view_class_mapping.items():
            for class_ in classes:
                mapping[class_] = view
        return mapping
