# Created by Alexander Watzinger and others. Please see README.md for licensing information
from collections import OrderedDict

from flask import g
from flask_login import current_user
from werkzeug.exceptions import abort

from openatlas import app, debug_model, logger
from openatlas.forms.date import DateForm
from openatlas.models.date import DateMapper
from openatlas.models.link import LinkMapper
from openatlas.util.util import print_file_extension, uc_first


class Entity:
    def __init__(self, row):
        if not row:
            logger.log('error', 'model', 'invalid id')
            abort(418)
        self.id = row.id
        self.nodes = dict()
        if hasattr(row, 'nodes') and row.nodes:
            for node in row.nodes:
                self.nodes[g.nodes[node['f1']]] = node['f2']  # f1 = node id, f2 = value
        self.name = row.name
        self.root = None
        self.description = row.description if row.description else ''
        self.system_type = row.system_type
        self.created = row.created
        self.modified = row.modified
        self.begin_from = None
        self.begin_to = None
        self.begin_comment = None
        self.end_from = None
        self.end_to = None
        self.end_comment = None
        if hasattr(row, 'begin_from'):
            self.begin_from = DateMapper.timestamp_to_datetime64(row.begin_from)
            self.begin_to = DateMapper.timestamp_to_datetime64(row.begin_to)
            self.begin_comment = row.begin_comment
            self.end_from = DateMapper.timestamp_to_datetime64(row.end_from)
            self.end_to = DateMapper.timestamp_to_datetime64(row.end_to)
            self.end_comment = row.end_comment
            self.first = DateForm.format_date(self.begin_from, 'year') if self.begin_from else None
            self.last = DateForm.format_date(self.end_from, 'year') if self.end_from else None
            self.last = DateForm.format_date(self.end_to, 'year') if self.end_to else self.last
        self.class_ = g.classes[row.class_code]
        self.view_name = None  # view_name is used to build urls
        if self.system_type == 'file':
            self.view_name = 'file'
        elif self.class_.code in app.config['CODE_CLASS']:
            self.view_name = app.config['CODE_CLASS'][self.class_.code]
        self.table_name = self.view_name  # table_name is used to build tables
        if self.view_name == 'place':
            self.table_name = self.system_type.replace(' ', '-')

    def get_linked_entity(self, code, inverse=False):
        return LinkMapper.get_linked_entity(self, code, inverse)

    def get_linked_entities(self, code, inverse=False):
        return LinkMapper.get_linked_entities(self, code, inverse)

    def link(self, code, range_, description=None, inverse=False):
        return LinkMapper.insert(self, code, range_, description, inverse)

    def get_links(self, code, inverse=False):
        return LinkMapper.get_links(self, code, inverse)

    def delete(self):
        EntityMapper.delete(self.id)

    def delete_links(self, codes):
        LinkMapper.delete_by_codes(self, codes)

    def update(self):
        EntityMapper.update(self)

    def save_nodes(self, form):
        from openatlas.models.node import NodeMapper
        NodeMapper.save_entity_nodes(self, form)

    def set_dates(self, form):
        self.begin_from = None
        self.begin_to = None
        self.begin_comment = None
        self.end_from = None
        self.end_to = None
        self.end_comment = None
        if form.begin_year_from.data:  # Only if begin year is set create a begin date or time span
            self.begin_from = DateMapper.form_to_datetime64(
                form.begin_year_from.data, form.begin_month_from.data, form.begin_day_from.data)
            self.begin_to = DateMapper.form_to_datetime64(
                form.begin_year_to.data, form.begin_month_to.data, form.begin_day_to.data)
            self.begin_comment = form.begin_comment.data
        if form.end_year_from.data:  # Only if end year is set create a year date or time span
            self.end_from = DateMapper.form_to_datetime64(
                form.end_year_from.data, form.end_month_from.data, form.end_day_from.data)
            self.end_to = DateMapper.form_to_datetime64(
                form.end_year_to.data, form.end_month_to.data, form.end_day_to.data)
            self.end_comment = form.end_comment.data

    def get_profile_image_id(self):
        return EntityMapper.get_profile_image_id(self.id)

    def remove_profile_image(self):
        return EntityMapper.remove_profile_image(self.id)

    def print_base_type(self):
        from openatlas.models.node import NodeMapper
        if not self.view_name or self.view_name == 'actor':  # actors have no base type
            return ''
        root_name = self.view_name.title()
        if self.view_name == 'reference':
            root_name = self.system_type.title()
        elif self.view_name == 'file':
            root_name = 'License'
        elif self.view_name == 'place':
            root_name = uc_first(self.system_type)
            if self.system_type == 'stratigraphic unit':
                root_name = 'Stratigraphic Unit'
        root_id = NodeMapper.get_hierarchy_by_name(root_name).id
        for node in self.nodes:
            if node.root and node.root[-1] == root_id:
                return node.name
        return ''

    def get_name_directed(self, inverse=False):
        """ Returns name part of a directed type e.g. Actor Actor Relation: Parent of (Child of)"""
        from openatlas.util.util import sanitize
        name_parts = self.name.split(' (')
        if inverse and len(name_parts) > 1:  # pragma: no cover
            return sanitize(name_parts[1], 'node')
        return name_parts[0]


class EntityMapper:
    sql = """
        SELECT
            e.id, e.class_code, e.name, e.description, e.created, e.modified, e.system_type,
            COALESCE(to_char(e.begin_from, 'yyyy-mm-dd BC'), '') AS begin_from, e.begin_comment,
            COALESCE(to_char(e.begin_to, 'yyyy-mm-dd BC'), '') AS begin_to,
            COALESCE(to_char(e.end_from, 'yyyy-mm-dd BC'), '') AS end_from, e.end_comment,
            COALESCE(to_char(e.end_to, 'yyyy-mm-dd BC'), '') AS end_to,
            array_to_json(
                array_agg((t.range_id, t.description)) FILTER (WHERE t.range_id IS NOT NULL)
            ) as nodes
        FROM model.entity e
        LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code IN ('P2', 'P89')"""

    sql_orphan = """
        SELECT e.id FROM model.entity e
        LEFT JOIN model.link l1 on e.id = l1.domain_id
        LEFT JOIN model.link l2 on e.id = l2.range_id
        WHERE l1.domain_id IS NULL AND l2.range_id IS NULL AND e.class_code != 'E55'"""

    @staticmethod
    def update(entity):
        from openatlas.util.util import sanitize
        sql = """
            UPDATE model.entity SET
            (name, description, begin_from, begin_to, begin_comment, end_from, end_to, end_comment) 
                = (%(name)s, %(description)s, %(begin_from)s, %(begin_to)s, %(begin_comment)s, 
                %(end_from)s, %(end_to)s, %(end_comment)s)
            WHERE id = %(id)s;"""
        g.cursor.execute(sql, {
            'id': entity.id, 'name': entity.name,
            'begin_from': DateMapper.datetime64_to_timestamp(entity.begin_from),
            'begin_to': DateMapper.datetime64_to_timestamp(entity.begin_to),
            'end_from': DateMapper.datetime64_to_timestamp(entity.end_from),
            'end_to': DateMapper.datetime64_to_timestamp(entity.end_to),
            'begin_comment': entity.begin_comment, 'end_comment': entity.end_comment,
            'description': sanitize(entity.description, 'description')})
        debug_model['div sql'] += 1

    @staticmethod
    def get_by_system_type(system_type):
        sql = EntityMapper.sql
        sql += ' WHERE e.system_type = %(system_type)s GROUP BY e.id ORDER BY e.name;'
        g.cursor.execute(sql, {'system_type': system_type})
        debug_model['div sql'] += 1
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_display_files():
        sql = EntityMapper.sql + " WHERE e.system_type = 'file' GROUP BY e.id ORDER BY e.name;"
        g.cursor.execute(sql)
        debug_model['div sql'] += 1
        entities = []
        for row in g.cursor.fetchall():
            if print_file_extension(row.id)[1:] in app.config['DISPLAY_FILE_EXTENSIONS']:
                entities.append(Entity(row))
        return entities

    @staticmethod
    def insert(code, name, system_type=None, description=None):
        if not name:  # pragma: no cover
            logger.log('error', 'database', 'Insert entity without name and date')
            return
        sql = """
            INSERT INTO model.entity (name, system_type, class_code, description)
            VALUES (%(name)s, %(system_type)s, %(code)s, %(description)s)
            RETURNING id;"""
        params = {'name': name.strip(), 'code': code,
                  'system_type': system_type.strip() if system_type else None,
                  'description': description.strip() if description else None}
        g.cursor.execute(sql, params)
        debug_model['div sql'] += 1
        return EntityMapper.get_by_id(g.cursor.fetchone()[0])

    @staticmethod
    def get_by_id(entity_id, ignore_not_found=False):
        if entity_id in g.nodes:  # pragma: no cover, just in case a node is requested
            return g.nodes[entity_id]
        sql = EntityMapper.sql + ' WHERE e.id = %(id)s GROUP BY e.id ORDER BY e.name;'
        g.cursor.execute(sql, {'id': entity_id})
        debug_model['by id'] += 1
        if g.cursor.rowcount < 1 and ignore_not_found:
            return None  # pragma: no cover, only used where expected to avoid a 418 e.g. at logs
        return Entity(g.cursor.fetchone())

    @staticmethod
    def get_by_project_id(project_id):
        sql = """
            SELECT e.id, ie.origin_id, e.class_code, e.name, e.description, e.created, e.modified,
                e.system_type,
            array_to_json(
                array_agg((t.range_id, t.description)) FILTER (WHERE t.range_id IS NOT NULL)
            ) as nodes
            FROM model.entity e
            LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code IN ('P2', 'P89')
            JOIN import.entity ie ON e.id = ie.entity_id
            WHERE ie.project_id = %(id)s GROUP BY e.id, ie.origin_id ORDER BY e.name;"""
        g.cursor.execute(sql, {'id': project_id})
        debug_model['by id'] += 1
        entities = []
        for row in g.cursor.fetchall():
            entity = Entity(row)
            entity.origin_id = row.origin_id
            entities.append(entity)
        return entities

    @staticmethod
    def get_by_ids(entity_ids):
        if not entity_ids:
            return []
        sql = EntityMapper.sql + ' WHERE e.id IN %(ids)s GROUP BY e.id ORDER BY e.name;'
        g.cursor.execute(sql, {'ids': tuple(entity_ids)})
        debug_model['by id'] += 1
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_by_codes(class_name):
        if class_name == 'source':
            sql = EntityMapper.sql + """
                WHERE e.class_code IN %(codes)s AND e.system_type = 'source content'
                GROUP BY e.id ORDER BY e.name;"""
        elif class_name == 'reference':
            sql = EntityMapper.sql + """
                WHERE e.class_code IN %(codes)s AND e.system_type != 'file'
                GROUP BY e.id ORDER BY e.name;"""
        else:
            sql = EntityMapper.sql + """
                WHERE e.class_code IN %(codes)s GROUP BY e.id ORDER BY e.name;"""
        g.cursor.execute(sql, {'codes': tuple(app.config['CLASS_CODES'][class_name])})
        debug_model['by codes'] += 1
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def delete(entity):
        """ Triggers function model.delete_entity_related() for deleting related entities"""
        id_ = entity if type(entity) is int else entity.id
        g.cursor.execute('DELETE FROM model.entity WHERE id = %(id_)s;', {'id_': id_})
        debug_model['by id'] += 1

    @staticmethod
    def get_overview_counts():
        sql = """
            SELECT
            SUM(CASE WHEN
                class_code = 'E33' AND system_type = 'source content' THEN 1 END) AS source,
            SUM(CASE WHEN class_code IN ('E6', 'E7', 'E8', 'E12') THEN 1 END) AS event,
            SUM(CASE WHEN class_code IN ('E21', 'E74', 'E40') THEN 1 END) AS actor,
            SUM(CASE WHEN class_code = 'E18' THEN 1 END) AS place,
            SUM(CASE WHEN class_code IN ('E31', 'E84') AND system_type != 'file' THEN 1 END)
                AS reference,
            SUM(CASE WHEN class_code = 'E31' AND system_type = 'file' THEN 1 END) AS file
            FROM model.entity;"""
        g.cursor.execute(sql)
        debug_model['div sql'] += 1
        row = g.cursor.fetchone()
        counts = OrderedDict()
        for idx, col in enumerate(g.cursor.description):
            counts[col[0]] = row[idx]
        return counts

    @staticmethod
    def get_orphans():
        """ Returns entities without links. """
        g.cursor.execute(EntityMapper.sql_orphan)
        debug_model['div sql'] += 1
        return [EntityMapper.get_by_id(row.id) for row in g.cursor.fetchall()]

    @staticmethod
    def get_latest(limit):
        """ Returns the newest created entities"""
        codes = []
        for class_codes in app.config['CLASS_CODES'].values():
            codes += class_codes
        sql = EntityMapper.sql + """
                WHERE e.class_code IN %(codes)s GROUP BY e.id
                ORDER BY e.created DESC LIMIT %(limit)s;"""
        g.cursor.execute(sql, {'codes': tuple(codes), 'limit': limit})
        debug_model['div sql'] += 1
        return [Entity(row) for row in g.cursor.fetchall()]

    @staticmethod
    def delete_orphans(parameter):
        from openatlas.models.node import NodeMapper
        class_codes = tuple(app.config['CODE_CLASS'].keys())
        if parameter == 'orphans':
            class_codes = class_codes + ('E55',)
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
        sql = 'DELETE FROM model.entity WHERE id IN (' + sql_where + ');'
        g.cursor.execute(sql, {'class_codes': class_codes})
        debug_model['div sql'] += 1
        return g.cursor.rowcount

    @staticmethod
    def search(form):
        sql = EntityMapper.sql
        if form.own.data:
            sql += " LEFT JOIN web.user_log ul ON e.id = ul.entity_id "
        sql += " WHERE LOWER(e.name) LIKE LOWER(%(term)s)"
        sql += " OR lower(e.description) LIKE lower(%(term)s) AND " if form.desc.data else " AND "
        sql += " ul.user_id = %(user_id)s AND " if form.own.data else ''
        sql += "("
        sql_where = []
        for name in form.classes.data:
            if name in ['source', 'event']:
                sql_where.append(" e.class_code IN ({codes})".format(
                    codes=str(app.config['CLASS_CODES'][name])[1:-1]))
            elif name == 'find':
                sql_where.append(" e.class_code = 'E22'")
            elif name == 'actor':
                codes = app.config['CLASS_CODES'][name] + ['E82']  # Add alias
                sql_where.append(" e.class_code IN ({codes})".format(codes=str(codes)[1:-1]))
            elif name in ['place', 'feature', 'stratigraphic unit']:
                sql_where.append(" e.class_code IN ('E18', 'E41')")
            elif name == 'reference':
                sql_where.append(" e.class_code IN ({codes}) AND e.system_type != 'file'".format(
                    codes=str(app.config['CLASS_CODES']['reference'])[1:-1]))
            elif name == 'file':
                sql_where.append(" e.system_type = 'file'")
        sql += ' OR '.join(sql_where) + ") GROUP BY e.id ORDER BY e.name;"
        g.cursor.execute(sql, {'term': '%' + form.term.data + '%', 'user_id': current_user.id})
        debug_model['div sql'] += 1
        entities = []
        for row in g.cursor.fetchall():
            if row.class_code == 'E82':  # If found in actor alias
                entities.append(LinkMapper.get_linked_entity(row.id, 'P131', True))
            elif row.class_code == 'E41':  # If found in place alias
                if 'place' in form.classes.data:  # Only places have alias
                    entities.append(LinkMapper.get_linked_entity(row.id, 'P1', True))
            elif row.class_code == 'E18':
                if row.system_type in form.classes.data:
                    entities.append(Entity(row))
            else:
                entities.append(Entity(row))
        return entities

    @staticmethod
    def set_profile_image(id_, origin_id):
        sql = """
            INSERT INTO web.entity_profile_image (entity_id, image_id)
            VALUES (%(entity_id)s, %(image_id)s)
            ON CONFLICT (entity_id) DO UPDATE SET image_id=%(image_id)s;"""
        g.cursor.execute(sql, {'entity_id': origin_id, 'image_id': id_})
        debug_model['div sql'] += 1

    @staticmethod
    def get_profile_image_id(id_):
        sql = 'SELECT image_id FROM web.entity_profile_image WHERE entity_id = %(entity_id)s;'
        g.cursor.execute(sql, {'entity_id': id_})
        debug_model['div sql'] += 1
        return g.cursor.fetchone()[0] if g.cursor.rowcount else None

    @staticmethod
    def remove_profile_image(entity_id):
        sql = 'DELETE FROM web.entity_profile_image WHERE entity_id = %(entity_id)s;'
        g.cursor.execute(sql, {'entity_id': entity_id})
        debug_model['div sql'] += 1

    @staticmethod
    def get_circular():
        # Get entities that are linked to itself
        g.cursor.execute('SELECT domain_id FROM model.link WHERE domain_id = range_id;')
        debug_model['div sql'] += 1
        return [EntityMapper.get_by_id(row.domain_id) for row in g.cursor.fetchall()]
