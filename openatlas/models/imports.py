from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, List, Optional

from flask import g
from flask_login import current_user
from psycopg2.extras import NamedTupleCursor

from openatlas.util.util import is_float


class Project:

    def __init__(self, row: NamedTupleCursor.Record) -> None:
        self.id = row.id
        self.name = row.name
        self.count = row.count
        self.description = row.description if row.description else ''
        self.created = row.created
        self.modified = row.modified


class Import:
    sql = """
        SELECT p.id, p.name, p.description, p.created, p.modified, COUNT(e.id) AS count
        FROM import.project p LEFT JOIN import.entity e ON p.id = e.project_id """

    @staticmethod
    def insert_project(name: str, description: Optional[str] = None) -> NamedTupleCursor.Record:
        description = description.strip() if description else None
        sql = """
            INSERT INTO import.project (name, description) VALUES (%(name)s, %(description)s)
            RETURNING id;"""
        g.execute(sql, {'name': name, 'description': description})
        return g.cursor.fetchone()[0]

    @staticmethod
    def get_all_projects() -> List[Project]:
        g.execute(Import.sql + ' GROUP by p.id ORDER BY name;')
        return [Project(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_project_by_id(id_: int) -> Project:
        g.execute(Import.sql + ' WHERE p.id = %(id)s GROUP by p.id;', {'id': id_})
        return Project(g.cursor.fetchone())

    @staticmethod
    def get_project_by_name(name: str) -> Optional[Project]:
        g.execute(Import.sql + ' WHERE p.name = %(name)s GROUP by p.id;', {'name': name})
        return Project(g.cursor.fetchone()) if g.cursor.rowcount == 1 else None

    @staticmethod
    def delete_project(id_: int) -> None:
        g.execute('DELETE FROM import.project WHERE id = %(id)s;', {'id': id_})

    @staticmethod
    def check_origin_ids(project: Project, origin_ids: List[str]) -> List[str]:
        """ Check if origin ids already in database"""
        sql = """
            SELECT origin_id FROM import.entity
            WHERE project_id = %(project_id)s AND origin_id IN %(ids)s;"""
        g.execute(sql, {'project_id': project.id, 'ids': tuple(set(origin_ids))})
        return [row.origin_id for row in g.cursor.fetchall()]

    @staticmethod
    def check_duplicates(class_code: str, names: List[str]) -> List[str]:
        sql = """
            SELECT DISTINCT name FROM model.entity
            WHERE class_code = %(class_code)s AND LOWER(name) IN %(names)s;"""
        g.execute(sql, {'class_code': class_code, 'names': tuple(names)})
        return [row.name for row in g.cursor.fetchall()]

    @staticmethod
    def update_project(project: Project) -> None:
        from openatlas.util.util import sanitize
        sql = """
            UPDATE import.project SET (name, description) = (%(name)s, %(description)s)
            WHERE id = %(id)s;"""
        g.execute(sql, {'id': project.id,
                        'name': project.name,
                        'description': sanitize(project.description, 'description')})

    @staticmethod
    def import_data(project: 'Project', class_code: str, data: List[Any]) -> None:
        from openatlas.models.entity import Entity
        from openatlas.models.gis import Gis
        for row in data:
            system_type = None
            if class_code == 'E33':  # pragma: no cover
                system_type = 'source content'
            elif class_code == 'E18':
                system_type = 'place'
            desc = row['description'] if 'description' in row and row['description'] else None
            entity = Entity.insert(class_code, row['name'], system_type, desc)
            sql = """
                INSERT INTO import.entity (project_id, origin_id, entity_id, user_id)
                VALUES (%(project_id)s, %(origin_id)s, %(entity_id)s, %(user_id)s);"""
            g.execute(sql, {'project_id': project.id,
                            'entity_id': entity.id,
                            'user_id': current_user.id,
                            'origin_id': row['id'] if 'id' in row and row['id'] else None})

            # Dates
            if 'begin_from' in row and row['begin_from']:
                entity.begin_from = row['begin_from']
                if 'begin_to' in row and row['begin_to']:
                    entity.begin_to = row['begin_to']
                if 'begin_comment' in row and row['begin_comment']:
                    entity.begin_comment = row['begin_comment']
            if 'end_from' in row and row['end_from']:
                entity.end_from = row['end_from']
                if 'end_to' in row and row['end_to']:
                    entity.end_to = row['end_to']
                if 'end_comment' in row and row['end_comment']:
                    entity.end_comment = row['end_comment']
            entity.update()

            # GIS
            if class_code == 'E18':
                location = Entity.insert('E53', 'Location of ' + row['name'], 'place location')
                entity.link('P53', location)
                if 'easting' in row and is_float(row['easting']):
                    if 'northing' in row and is_float(row['northing']):
                        Gis.insert_import(entity=entity,
                                          location=location,
                                          project=project,
                                          easting=row['easting'],
                                          northing=row['northing'])
