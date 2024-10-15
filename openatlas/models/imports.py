from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Optional

from flask import g
from flask_login import current_user
from shapely import wkt
from shapely.errors import WKTReadingError

from openatlas.api.import_scripts.util import (
    get_match_types, get_reference_system_by_name)
from openatlas.api.resources.api_entity import ApiEntity
from openatlas.api.resources.error import EntityDoesNotExistError
from openatlas.database import imports as db
from openatlas.display.util2 import sanitize
from openatlas.models.entity import Entity
from openatlas.models.gis import Gis


class Project:
    def __init__(self, row: dict[str, Any]) -> None:
        self.id = row['id']
        self.name = row['name']
        self.count = row['count']
        self.description = row['description'] or ''
        self.created = row['created']
        self.modified = row['modified']

    def update(self) -> None:
        db.update_project(
            self.id,
            self.name,
            sanitize(self.description, 'text') if self.description else None)

    @staticmethod
    def get_all() -> list[Project]:
        return [Project(row) for row in db.get_all_projects()]

    @staticmethod
    def get_by_id(id_: int) -> Project:
        return Project(db.get_project_by_id(id_))

    @staticmethod
    def get_by_name(name: str) -> Optional[Project]:
        row = db.get_project_by_name(name)
        return Project(row) if row else None

    @staticmethod
    def delete(id_: int) -> None:
        db.delete_project(id_)

    @staticmethod
    def insert(name: str, description: Optional[str] = None) -> int:
        return db.insert_project(
            name,
            sanitize(description, 'text') if description else None)


def get_origin_ids(project: Project, origin_ids: list[str]) -> list[str]:
    return db.check_origin_ids(project.id, origin_ids)


def check_duplicates(class_: str, names: list[str]) -> list[str]:
    return db.check_duplicates(class_, names)


def check_type_id(type_id: str, class_: str) -> bool:
    if not type_id.isdigit() or int(type_id) not in g.types:
        return False
    if not g.types[int(type_id)].root:
        return False
    root_type = g.types[g.types[int(type_id)].root[-1]]
    if class_ not in root_type.classes:
        return False
    if root_type.name in ['Administrative unit', 'Historical place']:
        return False
    return True


def check_single_type_duplicates(type_ids: list[str]) -> list[str]:
    single_types = defaultdict(list)
    for type_id in type_ids:
        if not g.types[int(type_id)].multiple:
            single_types[
                g.types[g.types[int(type_id)].root[-1]].name].append(type_id)
    single_type_ids = []
    for value in single_types.values():
        if len(value) > 1:
            single_type_ids.extend(value)
    return single_type_ids


def import_data_(project: Project, class_: str, data: list[Any]) -> None:
    entities: dict[str | int, dict[str, Any]] = {}
    for row in data:
        if value := row.get('openatlas_class'):
            if (value.lower().replace(' ', '_') in (
                    g.view_class_mapping['place'] +
                    g.view_class_mapping['artifact'])):
                class_ = value.lower().replace(' ', '_')
        entity = Entity.insert(class_, row['name'], row.get('description'))
        db.import_data(
            project.id,
            entity.id,
            current_user.id,
            origin_id=row.get('id'))
        if class_ in ['place', 'person', 'group']:
            insert_alias(entity, row)
        insert_dates(entity, row)
        link_types(entity, row, class_)
        link_references(entity, row, class_)
        if class_ in g.view_class_mapping['place'] \
                + g.view_class_mapping['artifact']:
            insert_gis(entity, row, project)
        entities[row.get('id')] = {
            'entity': entity,
            'parent_id': row.get('parent_id'),
            'openatlas_parent_id':  row.get('openatlas_parent_id')}
    for entry in entities.values():
        if entry['parent_id']:
            entities[entry['parent_id']]['entity'].link(
                'P46',
                entry['entity'])
        if entry['openatlas_parent_id']:
            Entity.get_by_id(entry['openatlas_parent_id']).link(
                'P46',
                entry['entity'])


def insert_dates(entity: Entity, row: dict[str, Any]) -> None:
    entity.update({'attributes': {
        'begin_from': row.get('begin_from'),
        'begin_to': row.get('begin_to'),
        'begin_comment': row.get('begin_comment'),
        'end_from': row.get('end_from'),
        'end_to': row.get('end_to'),
        'end_comment': row.get('end_comment')}})


def insert_alias(entity: Entity, row: dict[str, Any]) -> None:
    if aliases := row.get('alias'):
        for alias_ in aliases.split(";"):
            entity.link('P1', Entity.insert('appellation', alias_))


def link_types(entity: Entity, row: dict[str, Any], class_: str) -> None:
    if type_ids := row.get('type_ids'):
        for type_id in str(type_ids).split():
            if check_type_id(type_id, class_):
                entity.link('P2', g.types[int(type_id)])
    if data := row.get('value_types'):
        for value_types in str(data).split():
            value_type = value_types.split(';')
            number = value_type[1][1:] \
                if value_type[1].startswith('-') else value_type[1]
            if check_type_id(value_type[0], class_) and \
                    (number.isdigit() or number.replace('.', '', 1).isdigit()):
                entity.link('P2', g.types[int(value_type[0])], value_type[1])


def link_references(entity: Entity, row: dict[str, Any], class_: str) -> None:
    if data := row.get('references'):
        for references in clean_reference_pages(str(data)):
            reference = references.split(';')
            if len(reference) <= 2 and reference[0].isdigit():
                try:
                    ref_entity = ApiEntity.get_by_id(int(reference[0]))
                except EntityDoesNotExistError:
                    continue
                page = reference[1] or None
                ref_entity.link('P67', entity, page)
    match_types = get_match_types()
    systems = list(set(i for i in row if i.startswith('reference_system_')))
    for header in systems:
        system = header.replace('reference_system_', '')
        if reference_system := get_reference_system_by_name(system):
            if ((data := row.get(header)) and
                    class_ in reference_system.classes):
                values = data.split(';')
                if values[1] in match_types:
                    reference_system.link(
                        'P67',
                        entity,
                        values[0],
                        type_id=match_types[values[1]].id)


def insert_gis(entity: Entity, row: dict[str, Any], project: Project) -> None:
    location = Entity.insert('object_location', f"Location of {row['name']}")
    entity.link('P53', location)
    if data := row.get('administrative_unit'):
        if ((str(data).isdigit() and int(data) in g.types) and
                g.types[g.types[int(data)].root[-1]].name in [
                    'Administrative unit']):
            location.link('P89', g.types[int(data)])
    if data := row.get('historical_place'):
        if ((str(data).isdigit() and int(data) in g.types) and
                g.types[g.types[int(data)].root[-1]].name in [
                    'Historical place']):
            location.link('P89', g.types[int(data)])
    if coordinates := row.get('wkt'):
        try:
            wkt_ = wkt.loads(coordinates)
        except WKTReadingError:
            wkt_ = None
        if wkt_:
            if wkt_.geom_type in [
                    'MultiPoint',
                    'MultiLineString',
                    'MultiPolygon',
                    'GeometryCollection']:
                for poly in wkt_:
                    Gis.insert_wkt(entity, location, project, poly)
            else:
                Gis.insert_wkt(entity, location, project, wkt_)


def clean_reference_pages(value: str) -> list[str]:
    return re.findall(r'\d+;.*?(?=\d+;|$)', value)
