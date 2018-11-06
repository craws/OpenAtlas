# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import g
from flask_login import current_user


class Project:

    def __init__(self, row=None):
        self.id = None
        self.name = None
        if not row:
            return
        self.id = row.id
        self.name = row.name
        self.count = row.count
        self.description = row.description if row.description else ''
        self.created = row.created
        self.modified = row.modified


class ImportMapper:
    sql = """
        SELECT p.id, p.name, p.description, p.created, p.modified, COUNT(e.id) AS count
        FROM import.project p LEFT JOIN import.entity e ON p.id = e.project_id """

    @staticmethod
    def insert_project(name, description=None):
        description = description.strip() if description else None
        sql = """
            INSERT INTO import.project (name, description) VALUES (%(name)s, %(description)s)
            RETURNING id;"""
        g.cursor.execute(sql, {'name': name, 'description': description})
        return g.cursor.fetchone()[0]

    @staticmethod
    def get_all_projects():
        g.cursor.execute(ImportMapper.sql + ' GROUP by p.id ORDER BY name;')
        projects = []
        for row in g.cursor.fetchall():
            projects.append(Project(row))
        return projects

    @staticmethod
    def get_project_by_id(id_):
        g.cursor.execute(ImportMapper.sql + ' WHERE p.id = %(id)s GROUP by p.id;', {'id': id_})
        return Project(g.cursor.fetchone())

    @staticmethod
    def get_project_by_name(name):
        sql = ImportMapper.sql + ' WHERE p.name = %(name)s GROUP by p.id;'
        g.cursor.execute(sql, {'name': name})
        return Project(g.cursor.fetchone()) if g.cursor.rowcount == 1 else None

    @staticmethod
    def delete_project(id_):
        g.cursor.execute('DELETE FROM import.project WHERE id = %(id)s;', {'id': id_})

    @staticmethod
    def check_origin_ids(project, origin_ids):
        sql = """
            SELECT origin_id FROM import.entity
            WHERE project_id = %(project_id)s AND origin_id IN %(ids)s;"""
        g.cursor.execute(sql, {'project_id': project.id, 'ids': tuple(origin_ids)})
        existing = []
        for row in g.cursor.fetchall():
            existing.append(row.origin_id)
        return existing

    @staticmethod
    def check_duplicates(class_code, names):
        sql = """
            SELECT DISTINCT name FROM model.entity
            WHERE class_code = %(class_code)s AND LOWER(name) IN %(names)s;"""
        g.cursor.execute(sql, {'class_code': class_code, 'names': tuple(names)})
        return [row.name for row in g.cursor.fetchall()]

    @staticmethod
    def update_project(project):
        from openatlas.util.util import sanitize
        sql = """
            UPDATE import.project SET (name, description) = (%(name)s, %(description)s)
            WHERE id = %(id)s;"""
        g.cursor.execute(sql, {
            'id': project.id,
            'name': project.name,
            'description': sanitize(project.description, 'description')})

    @staticmethod
    def import_data(project, class_code, data):
        from openatlas.models.entity import EntityMapper
        for row in data:
            system_type = None
            if class_code == 'E33':  # pragma: no cover
                system_type = 'source content'
            elif class_code == 'E18':
                system_type = 'place'
            desc = row['description'] if 'description' in row and row['description'] else None
            entity = EntityMapper.insert(code=class_code, name=row['name'], description=desc,
                                         system_type=system_type)
            sql = """
                INSERT INTO import.entity (project_id, origin_id, entity_id, user_id)
                VALUES (%(project_id)s, %(origin_id)s, %(entity_id)s, %(user_id)s);"""
            g.cursor.execute(sql, {
                'project_id': project.id,
                'origin_id': row['id'] if 'id' in row and row['id'] else None,
                'entity_id': entity.id,
                'user_id': current_user.id})
            if class_code == 'E18':
                location = EntityMapper.insert('E53', 'Location of ' + row['name'],
                                               'place location')
                entity.link('P53', location)
