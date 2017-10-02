# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast
from collections import OrderedDict
import openatlas
from openatlas.models.date import DateMapper
from .classObject import ClassMapper


class Entity(object):
    def __init__(self, row):
        self.id = row.id
        self.types = []
        if hasattr(row, 'types') and self.types:
            for node_id in ast.literal_eval('[' + row.types + ']'):
                self.types.append(openatlas.nodes[node_id])
        self.name = row.name
        self.description = row.description if row.description else ''
        self.created = row.created
        self.modified = row.modified
        self.first = int(row.first) if hasattr(row, 'first') and row.first else None
        self.last = int(row.last) if hasattr(row, 'last') and row.last else None
        self.class_ = openatlas.classes[row.class_id]
        self.dates = {}

    def update(self):
        EntityMapper.update(self)

    def save_dates(self, form):
        DateMapper.save_dates(self, form)

    def save_nodes(self, form):
        openatlas.models.node.NodeMapper.save_nodes(self, form)

    def delete_nodes(self):
        openatlas.models.node.NodeMapper.delete_nodes(self)

    def delete_dates(self):
        DateMapper.delete_dates(self)

    def set_dates(self):
        self.dates = DateMapper.get_dates(self)


class EntityMapper(object):

    # To do: performance - refactor sub selects, get_by_class
    # To do: performance - use first and last only for get_by_codes?
    sql = """
        SELECT
            e.id, e.class_id, e.name, e.description, e.created, e.modified, c.code, e.value_timestamp, e.value_integer,
            string_agg(CAST(t.id AS text), ',') AS types,
            min(date_part('year', d1.value_timestamp)) AS first,
            max(date_part('year', d2.value_timestamp)) AS last

        FROM model.entity e
        JOIN model.class c ON e.class_id = c.id

        LEFT JOIN model.link tl ON e.id = tl.domain_id
        LEFT JOIN model.entity t ON
            tl.range_id = t.id AND tl.property_id = (SELECT id FROM model.property WHERE code = 'P2')

        LEFT JOIN model.link dl1 ON e.id = dl1.domain_id AND
            dl1.property_id IN (SELECT id FROM model.property WHERE code in ('OA1', 'OA3', 'OA5'))
        LEFT JOIN model.entity d1 ON dl1.range_id = d1.id

        LEFT JOIN model.link dl2 ON e.id = dl2.domain_id
            AND dl2.property_id IN (SELECT id FROM model.property WHERE code in ('OA2', 'OA4', 'OA6'))
        LEFT JOIN model.entity d2 ON dl2.range_id = d2.id
    """

    @staticmethod
    def update(entity):
        sql = "UPDATE model.entity SET (name, description) = (%(name)s, %(description)s) WHERE id = %(id)s;"
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': entity.id, 'name': entity.name, 'description': entity.description})

    @staticmethod
    def insert(code, name, description=None, date=None):
        if date:
            name = str(date)
        sql = """
            INSERT INTO model.entity (name, description, class_id, value_timestamp) VALUES (
                %(name)s,
                %(description)s,
                (SELECT id FROM model.class WHERE code = %(code)s),
                %(value_timestamp)s
            ) RETURNING id;"""
        params = {
            'name': name.strip(),
            'code': code,
            'description': description.strip() if description else None,
            'value_timestamp': date
        }
        cursor = openatlas.get_cursor()
        cursor.execute(sql, params)
        return EntityMapper.get_by_id(cursor.fetchone()[0])

    @staticmethod
    def get_by_id(entity_id):
        sql = EntityMapper.sql + 'WHERE e.id = %(id)s GROUP BY e.id, c.code ORDER BY e.name;'
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': entity_id})
        openatlas.debug_model['by id'] += 1
        return Entity(cursor.fetchone())

    @staticmethod
    def get_by_codes(codes):
        class_ids = []
        for code in codes if isinstance(codes, list) else [codes]:
            class_ids.append(ClassMapper.get_by_code(code).id)
        sql = EntityMapper.sql + " WHERE e.class_id IN %(class_ids)s GROUP BY e.id, c.code ORDER BY e.name;"
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'class_ids': tuple(class_ids)})
        entities = []
        for row in cursor.fetchall():
            entities.append(Entity(row))
        openatlas.debug_model['by codes'] += 1
        return entities

    @staticmethod
    def delete(entity_id):
        sql = "DELETE FROM model.entity WHERE id = %(entity_id)s;"
        openatlas.get_cursor().execute(sql, {'entity_id': entity_id})

    @staticmethod
    def get_overview_counts():
        sql = """
            SELECT
            (SELECT COUNT(*) FROM model.entity e JOIN model.class c ON e.class_id = c.id
                WHERE c.code = 'E33') AS source,
            (SELECT COUNT(*) FROM model.entity e JOIN model.class c ON e.class_id = c.id
                WHERE c.code IN ('E6', 'E7', 'E8', 'E12')) AS event,
            (SELECT COUNT(*) FROM model.entity e JOIN model.class c ON e.class_id = c.id
                WHERE c.code IN ('E21', 'E74', 'E40')) AS actor,
            (SELECT COUNT(*) FROM model.entity e JOIN model.class c ON e.class_id = c.id
                WHERE c.code = 'E18') AS place,
            COUNT(*) AS reference FROM model.entity e JOIN model.class c ON e.class_id = c.id
                WHERE c.code IN ('E31', 'E84');"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        counts = OrderedDict()  # To do: one liner possible to get a dict of record?
        for idx, col in enumerate(cursor.description):
            counts[col[0]] = row[idx]
        return counts
