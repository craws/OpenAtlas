# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import g


class Project:

    def __init__(self, row=None):
        self.id = None
        self.name = None
        if not row:
            return
        self.id = row.id
        self.nodes = dict()
        self.name = row.name
        self.description = row.description if row.description else ''
        self.created = row.created
        self.modified = row.modified


class ImportMapper:
    sql = """SELECT p.id, p.name, p.description, p.created, p.modified
            FROM import.project p"""

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
        g.cursor.execute(ImportMapper.sql + ' ORDER BY name;')
        projects = []
        for row in g.cursor.fetchall():
            projects.append(Project(row))
        return projects

    @staticmethod
    def get_project_by_id(id_):
        g.cursor.execute(ImportMapper.sql + ' WHERE p.id = %(id)s;', {'id': id_})
        return Project(g.cursor.fetchone())

    @staticmethod
    def get_project_by_name(name):
        g.cursor.execute(ImportMapper.sql + ' WHERE p.name = %(name)s;', {'name': name})
        return Project(g.cursor.fetchone()) if g.cursor.rowcount == 1 else None

    @staticmethod
    def delete_project(id_):
        g.cursor.execute('DELETE FROM import.project WHERE id = %(id)s;', {'id': id_})

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
