# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import ast
from collections import OrderedDict

from flask_login import current_user
from werkzeug.exceptions import abort

import openatlas
from openatlas import app
from openatlas.models.date import DateMapper
from openatlas.models.link import LinkMapper


class Entity:
    def __init__(self, row):
        if not row:
            openatlas.logger.log('error', 'model', 'invalid id')
            abort(418)
        self.id = row.id
        self.nodes = []
        if hasattr(row, 'types') and row.types:
            nodes_list = ast.literal_eval('[' + row.types + ']')
            # converting nodes_list to set, to list to avoid duplicates (from the sql statement)
            for node_id in list(set(nodes_list)):
                self.nodes.append(openatlas.nodes[node_id])
        self.name = row.name
        self.root = None
        self.description = row.description if row.description else ''
        self.system_type = row.system_type
        self.created = row.created
        self.modified = row.modified
        self.first = int(row.first) if hasattr(row, 'first') and row.first else None
        self.last = int(row.last) if hasattr(row, 'last') and row.last else None
        self.class_ = openatlas.classes[row.class_code]
        self.dates = {}

    def get_linked_entity(self, code, inverse=False):
        return LinkMapper.get_linked_entity(self, code, inverse)

    def get_linked_entities(self, code, inverse=False):
        return LinkMapper.get_linked_entities(self, code, inverse)

    def link(self, code, range_, description=None):
        return LinkMapper.insert(self, code, range_, description)

    def get_links(self, code, inverse=False):
        return LinkMapper.get_links(self, code, inverse)

    def delete(self):
        EntityMapper.delete(self.id)

    def delete_links(self, codes):
        LinkMapper.delete_by_codes(self, codes)

    def update(self):
        EntityMapper.update(self)

    def save_dates(self, form):
        DateMapper.save_dates(self, form)

    def save_nodes(self, form):
        openatlas.NodeMapper.save_entity_nodes(self, form)

    def set_dates(self):
        self.dates = DateMapper.get_dates(self)

    def print_base_type(self):
        if self.class_.code not in app.config['CODE_CLASS']:
            return ''
        if self.class_.code in app.config['CLASS_CODES']['actor']:
            return ''  # actors have no base type
        root_name = app.config['CODE_CLASS'][self.class_.code].title()
        if self.class_.code in app.config['CLASS_CODES']['reference']:
            root_name = self.system_type.title()
        root_id = openatlas.NodeMapper.get_hierarchy_by_name(root_name).id
        for node in self.nodes:
            if node.root and node.root[-1] == root_id:
                return node.name
        return ''

    def get_name_directed(self, inverse=False):
        """Returns name part of a directed type e.g. Actor Actor Relation: Parent of (Child of)"""
        from openatlas.util.util import sanitize
        name_parts = self.name.split(' (')
        if inverse and len(name_parts) > 1:
            return sanitize(name_parts[1], 'node')
        return name_parts[0]


class EntityMapper:
    # Todo: performance - refactor sub selects, get_by_class
    # Todo: performance - use first and last only for get_by_codes?
    sql = """
        SELECT
            e.id, e.class_code, e.name, e.description, e.created, e.modified,
            e.value_integer, e.system_type,
            string_agg(CAST(t.range_id AS text), ',') AS types,
            min(date_part('year', d1.value_timestamp)) AS first,
            max(date_part('year', d2.value_timestamp)) AS last

        FROM model.entity e
        LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code IN ('P2', 'P89')

        LEFT JOIN model.link dl1 ON e.id = dl1.domain_id
            AND dl1.property_code IN ('OA1', 'OA3', 'OA5')
        LEFT JOIN model.entity d1 ON dl1.range_id = d1.id

        LEFT JOIN model.link dl2 ON e.id = dl2.domain_id
            AND dl2.property_code IN ('OA2', 'OA4', 'OA6')
        LEFT JOIN model.entity d2 ON dl2.range_id = d2.id"""

    sql_orphan = """
        SELECT e.id FROM model.entity e
        LEFT JOIN model.link l1 on e.id = l1.domain_id
        LEFT JOIN model.link l2 on e.id = l2.range_id
        LEFT JOIN model.link_property lp2 on e.id = lp2.range_id
        WHERE
            l1.domain_id IS NULL AND
            l2.range_id IS NULL AND
            lp2.range_id IS NULL """

    @staticmethod
    def update(entity):
        from openatlas.util.util import sanitize
        sql = """
            UPDATE model.entity SET (name, description) = (%(name)s, %(description)s)
            WHERE id = %(id)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {
            'id': entity.id,
            'name': entity.name,
            'description': sanitize(entity.description, 'description')})

    @staticmethod
    def insert(code, name, system_type=None, description=None, date=None):
        if not name and not date:  # pragma: no cover
            openatlas.logger.log('error', 'database', 'Insert entity without name and date')
            return  # something went wrong so don't insert
        sql = """
            INSERT INTO model.entity (name, system_type, class_code, description, value_timestamp)
            VALUES (%(name)s, %(system_type)s, %(code)s, %(description)s, %(value_timestamp)s)
            RETURNING id;"""
        params = {
            'name': str(date) if date else name.strip(),
            'code': code,
            'system_type': system_type.strip() if system_type else None,
            'description': description.strip() if description else None,
            'value_timestamp':  DateMapper.datetime64_to_timestamp(date) if date else None}
        cursor = openatlas.get_cursor()
        cursor.execute(sql, params)
        return EntityMapper.get_by_id(cursor.fetchone()[0])

    @staticmethod
    def get_by_id(entity_id):
        sql = EntityMapper.sql + ' WHERE e.id = %(id)s GROUP BY e.id ORDER BY e.name;'
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': entity_id})
        openatlas.debug_model['by id'] += 1
        return Entity(cursor.fetchone())

    @staticmethod
    def get_by_ids(entity_ids):
        if not entity_ids:
            return []
        sql = EntityMapper.sql + ' WHERE e.id IN %(ids)s GROUP BY e.id ORDER BY e.name;'
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'ids': tuple(entity_ids)})
        openatlas.debug_model['by id'] += 1
        entities = []
        for row in cursor.fetchall():
            entities.append(Entity(row))
        return entities

    @staticmethod
    def get_by_codes(class_name):
        cursor = openatlas.get_cursor()
        if class_name == 'source':
            sql = EntityMapper.sql + """
                WHERE e.class_code IN %(codes)s AND e.system_type ='source content'
                GROUP BY e.id ORDER BY e.name;"""
        else:
            sql = EntityMapper.sql + """
                WHERE e.class_code IN %(codes)s GROUP BY e.id ORDER BY e.name;"""
        cursor.execute(sql, {'codes': tuple(app.config['CLASS_CODES'][class_name])})
        openatlas.debug_model['by codes'] += 1
        entities = []
        for row in cursor.fetchall():
            entities.append(Entity(row))
        return entities

    @staticmethod
    def delete(entity):
        """ Triggers function model.delete_entity_related() for deleting related entities"""
        entity_id = entity if isinstance(entity, int) else entity.id
        sql = "DELETE FROM model.entity WHERE id = %(entity_id)s;"
        openatlas.get_cursor().execute(sql, {'entity_id': entity_id})

    @staticmethod
    def get_overview_counts():
        sql = """
            SELECT
            SUM(CASE WHEN
                class_code = 'E33' AND system_type = 'source content' THEN 1 END) AS source,
            SUM(CASE WHEN class_code IN ('E6', 'E7', 'E8', 'E12') THEN 1 END) AS event,
            SUM(CASE WHEN class_code IN ('E21', 'E74', 'E40') THEN 1 END) AS actor,
            SUM(CASE WHEN class_code = 'E18' THEN 1 END) AS place,
            SUM(CASE WHEN class_code IN ('E31', 'E84') THEN 1 END) AS reference
            FROM model.entity;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        counts = OrderedDict()  # Todo: one liner to get a dict of record?
        for idx, col in enumerate(cursor.description):
            counts[col[0]] = row[idx]
        return counts

    @staticmethod
    def get_page_ids(entity, codes):
        """ Return ids for pager (first, previous, next, last)"""
        sql_where = " e.class_code IN ('{codes}')".format(codes="','".join(codes)) + " AND "
        sql_where += "e.system_type='source content'" if 'E33' in codes else "e.system_type IS NULL"
        sql_prev = "SELECT max(e.id) AS id FROM model.entity e WHERE e.id < %(id)s AND " + sql_where
        sql_next = "SELECT min(e.id) AS id FROM model.entity e WHERE e.id > %(id)s AND " + sql_where
        sql = """
            SELECT min(e.id) AS first_id, max(e.id) AS last_id,
                ({sql_next}) AS next_id, ({sql_prev}) AS previous_id
            FROM model.entity e WHERE """.format(
                sql_next=sql_next, sql_prev=sql_prev) + sql_where
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': entity.id})
        return cursor.fetchone()

    @staticmethod
    def get_orphans():
        """ Returns entities without links. """
        entities = []
        cursor = openatlas.get_cursor()
        cursor.execute(EntityMapper.sql_orphan)
        openatlas.debug_model['div sql'] += 1
        for row in cursor.fetchall():
            entities.append(EntityMapper.get_by_id(row.id))
        return entities

    @staticmethod
    def get_latest(limit):
        """ Returns the newest created entities"""
        codes = []
        for class_, class_codes in app.config['CLASS_CODES'].items():
            codes += class_codes
        sql = EntityMapper.sql + """
                WHERE e.class_code IN %(codes)s
                GROUP BY e.id
                ORDER BY e.created DESC LIMIT %(limit)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'codes': tuple(codes), 'limit': limit})
        openatlas.debug_model['div sql'] += 1
        entities = []
        for row in cursor.fetchall():
            entities.append(Entity(row))
        return entities

    @staticmethod
    def delete_orphans(parameter):
        from openatlas import app, NodeMapper
        if parameter == 'orphans':
            sql_where = EntityMapper.sql_orphan + " AND e.class_code NOT IN %(class_codes)s"
        elif parameter == 'unlinked':
            sql_where = EntityMapper.sql_orphan + " AND e.class_code IN %(class_codes)s"
        elif parameter == 'types':
            count = 0
            for node in NodeMapper.get_orphans():
                EntityMapper.delete(node)
                count += 1
            return count
        else:
            return 0
        sql = "DELETE FROM model.entity WHERE id IN (" + sql_where + ");"
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'class_codes': tuple(app.config['CODE_CLASS'].keys())})
        return cursor.rowcount

    @staticmethod
    def search(term, codes, description=False, own=False):
        sql = EntityMapper.sql
        if own:
            sql += " LEFT JOIN web.user_log ul ON e.id = ul.entity_id "
        sql += " WHERE LOWER(e.name) LIKE LOWER(%(term)s)"
        sql += " OR lower(e.description) LIKE lower(%(term)s) AND " if description else " AND "
        sql += " ul.user_id = %(user_id)s AND " if own else ''
        sql += " e.class_code IN %(codes)s"
        sql += " GROUP BY e.id ORDER BY e.name"
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {
            'term': '%' + term + '%',
            'codes': tuple(codes),
            'user_id': current_user.id})
        openatlas.debug_model['div sql'] += 1
        entities = []
        for row in cursor.fetchall():
            if row.class_code == 'E82':  # if found in actor alias
                entities.append(LinkMapper.get_linked_entity(row.id, 'P131', True))
            elif row.class_code == 'E41':  # if found in place alias
                entities.append(LinkMapper.get_linked_entity(row.id, 'P1', True))
            else:
                entities.append(Entity(row))
        return entities
