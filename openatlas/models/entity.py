# -*- coding: utf-8 -*-
import openatlas


class Entity(object):
    def __init__(self, row):
        self.id = row.id
        self.name = row.name
        self.description = row.description if row.description else ''
        self.created = row.created
        self.modified = row.modified
        self.begin = row.begin if hasattr(row, 'begin') else None
        self.end = row.end if hasattr(row, 'end') else None
        self.class_ = openatlas.classes[row.class_id]


class EntityMapper(object):

    @staticmethod
    def insert(code, name, description=None):
        sql = """
            INSERT INTO model.entity (name, description, class_id) VALUES (
                %(name)s,
                %(description)s,
                (SELECT id FROM model.class WHERE code = %(code)s)
            ) RETURNING id;"""
        params = {
            'name': name.strip(),
            'code': code,
            'description': description.strip() if description else None}
        cursor = openatlas.get_cursor()
        cursor.execute(sql, params)
        return EntityMapper.get_by_id(cursor.fetchone()[0])

    @staticmethod
    def get_by_id(entity_id):
        sql = """
            SELECT e.id, e.name, e.class_id, e.description, e.created, e.modified
            FROM model.entity e WHERE e.id = %(id)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': entity_id})
        openatlas.debug['by id'] += 1
        return Entity(cursor.fetchone())
