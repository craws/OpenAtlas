# Created by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import abort, flash, g
from flask_babel import lazy_gettext as _

from openatlas import debug_model, logger
from openatlas.forms.date import DateForm
from openatlas.models.date import DateMapper


class Link:

    def __init__(self, row, domain=None, range_=None):
        from openatlas.models.entity import EntityMapper
        self.id = row.id
        self.description = row.description
        self.property = g.properties[row.property_code]
        self.domain = domain if domain else EntityMapper.get_by_id(row.domain_id)
        self.range = range_ if range_ else EntityMapper.get_by_id(row.range_id)
        self.type = g.nodes[row.type_id] if row.type_id else None
        self.nodes = dict()
        if hasattr(row, 'type_id') and row.type_id:
            self.nodes[g.nodes[row.type_id]] = None
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

    def update(self):
        LinkMapper.update(self)

    def delete(self):
        LinkMapper.delete(self.id)

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
                form.begin_year_to.data, form.begin_month_to.data, form.begin_day_to.data, True)
            self.begin_comment = form.begin_comment.data
        if form.end_year_from.data:  # Only if end year is set create a year date or time span
            self.end_from = DateMapper.form_to_datetime64(
                form.end_year_from.data, form.end_month_from.data, form.end_day_from.data)
            self.end_to = DateMapper.form_to_datetime64(
                form.end_year_to.data, form.end_month_to.data, form.end_day_to.data, True)
            self.end_comment = form.end_comment.data


class LinkMapper:

    @staticmethod
    def insert(entity, property_code, linked_entities, description=None, inverse=False):
        from openatlas.models.entity import Entity, EntityMapper
        # linked_entities can be an entity, an entity id or a list of them
        if not entity or not linked_entities:  # pragma: no cover
            return
        property_ = g.properties[property_code]
        try:
            linked_entities = ast.literal_eval(linked_entities)
        except (SyntaxError, ValueError):
            pass
        linked_entities = linked_entities if type(linked_entities) is list else [linked_entities]
        if type(linked_entities[0]) is not Entity:
            linked_entities = EntityMapper.get_by_ids(linked_entities)
        result = None
        for linked_entity in linked_entities:
            domain = linked_entity if inverse else entity
            range_ = entity if inverse else linked_entity
            domain_error = True
            range_error = True
            if property_.find_object('domain_class_code', g.classes[domain.class_.code].code):
                domain_error = False
            if property_.find_object('range_class_code', g.classes[range_.class_.code].code):
                range_error = False
            if domain_error or range_error:
                text = _('error link') + ': ' + g.classes[domain.class_.code].code + ' > '
                text += property_code + ' > ' + g.classes[range_.class_.code].code
                logger.log('error', 'model', text)
                flash(text, 'error')
                continue
            sql = """
                INSERT INTO model.link (property_code, domain_id, range_id, description)
                VALUES (%(property_code)s, %(domain_id)s, %(range_id)s, %(description)s)
                RETURNING id;"""
            # Todo: build only one sql and get execution out of loop
            g.cursor.execute(sql, {'property_code': property_code, 'domain_id': domain.id,
                                   'range_id': range_.id, 'description': description})
            debug_model['link sql'] += 1
            result = g.cursor.fetchone()[0]
        return result

    @staticmethod
    def get_linked_entity(entity_param, code, inverse=False, nodes=False):
        result = LinkMapper.get_linked_entities(entity_param, code, inverse=inverse, nodes=nodes)
        if len(result) > 1:  # pragma: no cover
            logger.log('error', 'model', 'multiple linked entities found for ' + code)
            flash(_('error multiple linked entities found'), 'error')
            return
        if result:
            return result[0]

    @staticmethod
    def get_linked_entities(entity, codes, inverse=False, nodes=False):
        from openatlas.models.entity import EntityMapper
        sql = """
            SELECT range_id AS result_id FROM model.link
            WHERE domain_id = %(entity_id)s AND property_code IN %(codes)s;"""
        if inverse:
            sql = """
                SELECT domain_id AS result_id FROM model.link
                WHERE range_id = %(entity_id)s AND property_code IN %(codes)s;"""
        g.cursor.execute(sql, {
            'entity_id': entity if type(entity) is int else entity.id,
            'codes': tuple(codes if type(codes) is list else [codes])})
        debug_model['link sql'] += 1
        ids = [element for (element,) in g.cursor.fetchall()]
        return EntityMapper.get_by_ids(ids, nodes=nodes)

    @staticmethod
    def get_links(entity, codes, inverse=False):
        from openatlas.models.entity import EntityMapper
        sql = """
            SELECT l.id, l.property_code, l.domain_id, l.range_id, l.description, l.created,
                l.modified, e.name, l.type_id,
                COALESCE(to_char(l.begin_from, 'yyyy-mm-dd BC'), '') AS begin_from, l.begin_comment,
                COALESCE(to_char(l.begin_to, 'yyyy-mm-dd BC'), '') AS begin_to,
                COALESCE(to_char(l.end_from, 'yyyy-mm-dd BC'), '') AS end_from, l.end_comment,
                COALESCE(to_char(l.end_to, 'yyyy-mm-dd BC'), '') AS end_to
            FROM model.link l
            JOIN model.entity e ON l.{second}_id = e.id AND l.property_code IN %(codes)s
            WHERE l.{first}_id = %(entity_id)s GROUP BY l.id, e.name ORDER BY e.name;""".format(
            first='range' if inverse else 'domain', second='domain' if inverse else 'range')
        g.cursor.execute(sql, {
            'entity_id': entity if type(entity) is int else entity.id,
            'codes': tuple(codes if type(codes) is list else [codes])})
        debug_model['link sql'] += 1
        entity_ids = set()
        result = g.cursor.fetchall()
        for row in result:
            entity_ids.add(row.domain_id)
            entity_ids.add(row.range_id)
        entities = {entity.id: entity for entity in EntityMapper.get_by_ids(entity_ids)}
        links = []
        for row in result:
            links.append(Link(row, domain=entities[row.domain_id], range_=entities[row.range_id]))
        return links

    @staticmethod
    def delete_by_codes(entity, codes):
        codes = codes if type(codes) is list else [codes]
        sql = 'DELETE FROM model.link WHERE property_code IN %(codes)s AND domain_id = %(id)s;'
        g.cursor.execute(sql, {'id': entity.id, 'codes': tuple(codes)})
        debug_model['link sql'] += 1

    @staticmethod
    def get_by_id(id_):
        sql = """
            SELECT l.id, l.property_code, l.domain_id, l.range_id, l.description, l.created,
                l.modified, l.type_id,
                COALESCE(to_char(l.begin_from, 'yyyy-mm-dd BC'), '') AS begin_from, l.begin_comment,
                COALESCE(to_char(l.begin_to, 'yyyy-mm-dd BC'), '') AS begin_to,
                COALESCE(to_char(l.end_from, 'yyyy-mm-dd BC'), '') AS end_from, l.end_comment,
                COALESCE(to_char(l.end_to, 'yyyy-mm-dd BC'), '') AS end_to
            FROM model.link l
            WHERE l.id = %(id)s;"""
        g.cursor.execute(sql, {'id': id_})
        debug_model['link sql'] += 1
        return Link(g.cursor.fetchone())

    @staticmethod
    def get_entities_by_node(node):
        sql = "SELECT id, domain_id, range_id from model.link WHERE type_id = %(node_id)s;"
        g.cursor.execute(sql, {'node_id': node.id})
        debug_model['link sql'] += 1
        return g.cursor.fetchall()

    @staticmethod
    def delete(id_):
        from openatlas.util.util import is_authorized
        if not is_authorized('editor'):  # pragma: no cover
            abort(403)
        g.cursor.execute("DELETE FROM model.link WHERE id = %(id)s;", {'id': id_})
        debug_model['link sql'] += 1

    @staticmethod
    def update(link):
        sql = """
            UPDATE model.link SET (property_code, domain_id, range_id, description, type_id,
                begin_from, begin_to, begin_comment, end_from, end_to, end_comment) =
                (%(property_code)s, %(domain_id)s, %(range_id)s, %(description)s, %(type_id)s,
                 %(begin_from)s, %(begin_to)s, %(begin_comment)s, %(end_from)s, %(end_to)s,
                 %(end_comment)s)
            WHERE id = %(id)s;"""
        g.cursor.execute(sql, {'id': link.id,
                               'property_code': link.property.code,
                               'domain_id': link.domain.id,
                               'range_id': link.range.id,
                               'type_id': link.type.id if link.type else None,
                               'description': link.description,
                               'begin_from': DateMapper.datetime64_to_timestamp(link.begin_from),
                               'begin_to': DateMapper.datetime64_to_timestamp(link.begin_to),
                               'begin_comment': link.begin_comment,
                               'end_from':  DateMapper.datetime64_to_timestamp(link.end_from),
                               'end_to':  DateMapper.datetime64_to_timestamp(link.end_to),
                               'end_comment':  link.end_comment})
        debug_model['link sql'] += 1

    @staticmethod
    def check_links():
        """ Check all existing links for CIDOC CRM validity and return the invalid ones."""
        from openatlas.util.util import link
        from openatlas.models.entity import EntityMapper
        sql = """
            SELECT DISTINCT l.property_code AS property, d.class_code AS domain,
                r.class_code AS range
            FROM model.link l
            JOIN model.entity d ON l.domain_id = d.id
            JOIN model.entity r ON l.range_id = r.id;"""
        g.cursor.execute(sql)
        debug_model['link sql'] += 1
        invalid_links = []
        for row in g.cursor.fetchall():
            property_ = g.properties[row.property]
            domain_is_valid = property_.find_object('domain_class_code', row.domain)
            range_is_valid = property_.find_object('range_class_code', row.range)
            invalid_linking = []
            if not domain_is_valid or not range_is_valid:
                invalid_linking.append({
                    'property': row.property,
                    'domain': row.domain,
                    'range': row.range})
            for item in invalid_linking:
                sql = """
                    SELECT l.id, l.property_code, l.domain_id, l.range_id, l.description,
                        l.created, l.modified
                    FROM model.link l
                    JOIN model.entity d ON l.domain_id = d.id
                    JOIN model.entity r ON l.range_id = r.id
                    WHERE l.property_code = %(property)s
                        AND d.class_code = %(domain)s
                        AND r.class_code = %(range)s;"""
                g.cursor.execute(sql, {'property': item['property'], 'domain': item['domain'],
                                       'range': item['range']})
                debug_model['link sql'] += 1
                for row2 in g.cursor.fetchall():
                    domain = EntityMapper.get_by_id(row2.domain_id)
                    range_ = EntityMapper.get_by_id(row2.range_id)
                    invalid_links.append({'domain': link(domain) + ' (' + domain.class_.code + ')',
                                          'property': link(g.properties[row2.property_code]),
                                          'range': link(range_) + ' (' + range_.class_.code + ')'})
        return invalid_links

    @staticmethod
    def check_link_duplicates():
        # Find links with the same data (except id, created, modified)
        sql = """
            SELECT COUNT(*) AS count, domain_id, range_id, property_code, description, type_id,
                begin_from, begin_to, begin_comment, end_from, end_to, end_comment
            FROM model.link GROUP BY
                domain_id, range_id, property_code, description, type_id,
                begin_from, begin_to, begin_comment, end_from, end_to, end_comment
            HAVING COUNT(*) > 1"""
        g.cursor.execute(sql)
        debug_model['link sql'] += 1
        return g.cursor.fetchall()

    @staticmethod
    def delete_link_duplicates():
        # Delete duplicate links which may be artifacts from imports
        sql = """
        DELETE FROM model.link l WHERE l.id NOT IN (
            SELECT id FROM (
                SELECT DISTINCT ON (domain_id, range_id, property_code, description, type_id,
                    begin_from, begin_to, begin_comment, end_from, end_to, end_comment) *
                FROM model.link) AS temp_table);"""
        g.cursor.execute(sql)
        debug_model['link sql'] += 1
        return g.cursor.rowcount

    @staticmethod
    def check_single_type_duplicates():
        # Find entities with multiple types attached which should be single
        single_node_ids = []
        for id_, node in g.nodes.items():
            if not node.root:
                continue
            root = g.nodes[node.root[0]]
            if hasattr(root, 'multiple') and not root.multiple:
                single_node_ids.append(id_)
        sql = """
            SELECT COUNT(*) AS count, domain_id, range_id, type_id FROM model.link
            WHERE property_code = 'P2' AND (range_id IN %(node_ids)s OR type_id IN %(node_ids)s)
            GROUP BY domain_id, range_id, type_id
            HAVING COUNT(*) > 1"""
        g.cursor.execute(sql,{'node_ids': tuple(single_node_ids)})
        debug_model['link sql'] += 1
        return g.cursor.fetchall()
