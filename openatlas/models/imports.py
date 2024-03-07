from typing import Any, Optional

from flask import g
from flask_login import current_user

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


class Import:
    @staticmethod
    def insert_project(name: str, description: Optional[str] = None) -> int:
        return db.insert_project(
            name,
            description.strip() if description else None)

    @staticmethod
    def get_all_projects() -> list[Project]:
        return [Project(row) for row in db.get_all_projects()]

    @staticmethod
    def get_project_by_id(id_: int) -> Project:
        return Project(db.get_project_by_id(id_))

    @staticmethod
    def get_project_by_name(name: str) -> Optional[Project]:
        row = db.get_project_by_name(name)
        return Project(row) if row else None

    @staticmethod
    def delete_project(id_: int) -> None:
        db.delete_project(id_)

    @staticmethod
    def get_origin_ids(project: Project, origin_ids: list[str]) -> list[str]:
        return db.check_origin_ids(project.id, origin_ids)

    @staticmethod
    def check_duplicates(class_: str, names: list[str]) -> list[str]:
        return db.check_duplicates(class_, names)

    @staticmethod
    def update_project(project: Project) -> None:
        db.update_project(
            project.id,
            project.name,
            sanitize(project.description, 'text'))

    @staticmethod
    def check_type_id(type_id: str, class_: str) -> bool:
        if not type_id.isdigit() or int(type_id) not in g.types:
            return False
        if class_ not in g.types[
                g.types[int(type_id)].root[-1]].classes:  # pragma: no cover
            return False
        return True  # pragma: no cover

    @staticmethod
    def import_data(project: Project, class_: str, data: list[Any]) -> None:
        for row in data:
            entity = Entity.insert(
                class_,
                row['name'],
                row['description'] if 'description' in row else None)
            db.import_data(
                project.id,
                entity.id,
                current_user.id,
                origin_id=row['id'] if 'id' in row and row['id'] else None)

            # Dates
            dates = {
                'begin_from': None, 'begin_to': None, 'begin_comment': None,
                'end_from': None, 'end_to': None, 'end_comment': None}
            if 'begin_from' in row and row['begin_from']:
                dates['begin_from'] = row['begin_from']
                if 'begin_to' in row and row['begin_to']:
                    dates['begin_to'] = row['begin_to']
                if 'begin_comment' in row and row['begin_comment']:
                    dates['begin_comment'] = row['begin_comment']
            if 'end_from' in row and row['end_from']:
                dates['end_from'] = row['end_from']
                if 'end_to' in row and row['end_to']:
                    dates['end_to'] = row['end_to']
                if 'end_comment' in row and row['end_comment']:
                    dates['end_comment'] = row['end_comment']
            entity.update({'attributes': dates})

            # Types
            if 'type_ids' in row and row['type_ids']:
                for type_id in str(row['type_ids']).split():
                    if not Import.check_type_id(type_id, class_):
                        continue
                    entity.link('P2', g.types[int(type_id)])  # pragma no cover

            # GIS
            if class_ in ['place', 'artifact']:
                location = Entity.insert(
                    'object_location',
                    f"Location of {row['name']}")
                entity.link('P53', location)
                if 'easting' in row \
                        and is_float(row['easting']) \
                        and 'northing' in row \
                        and is_float(row['northing']):
                    Gis.insert_import(
                        entity=entity,
                        location=location,
                        project=project,
                        easting=row['easting'],
                        northing=row['northing'])


def is_float(value: int | float) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True
