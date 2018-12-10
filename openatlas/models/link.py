# Created by Alexander Watzinger and others. Please see README.md for licensing information
import ast

from flask import abort, flash, g
from flask_babel import lazy_gettext as _

from openatlas import debug_model, logger


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
        self.first = int(row.first) if hasattr(row, 'first') and row.first else None
        self.last = int(row.last) if hasattr(row, 'last') and row.last else None
        self.dates = {}

    def update(self):
        LinkMapper.update(self)

    def delete(self):
        LinkMapper.delete(self.id)

    def set_dates(self):
        from openatlas.models.date import DateMapper
        self.dates = DateMapper.get_link_dates(self)


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
            # Todo: build only sql and get execution out of loop
            g.cursor.execute(sql, {
                'property_code': property_code,
                'domain_id': domain.id,
                'range_id': range_.id,
                'description': description})
            debug_model['link sql'] += 1
            result = g.cursor.fetchone()[0]
        return result

    @staticmethod
    def get_linked_entity(entity_param, code, inverse=False):
        result = LinkMapper.get_linked_entities(entity_param, code, inverse)
        if len(result) > 1:  # pragma: no cover
            logger.log('error', 'model', 'multiple linked entities found for ' + code)
            flash(_('error multiple linked entities found'), 'error')
            return
        if result:
            return result[0]

    @staticmethod
    def get_linked_entities(entity, codes, inverse=False):
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
        return EntityMapper.get_by_ids(ids)

    @staticmethod
    def get_links(entity, codes, inverse=False):
        from openatlas.models.entity import EntityMapper
        sql = """
            SELECT l.id, l.property_code, l.domain_id, l.range_id, l.description, l.created,
                l.modified, e.name,
                min(date_part('year', d1.value_timestamp)) AS first,
                max(date_part('year', d2.value_timestamp)) AS last,
                (SELECT t.id FROM model.entity t
                    JOIN model.link_property lp ON t.id = lp.range_id
                        AND lp.domain_id = l.id
                        And lp.property_code = 'P2'
                ) AS type_id
            FROM model.link l
            JOIN model.entity e ON l.{second}_id = e.id AND l.property_code IN %(codes)s
            LEFT JOIN model.link_property dl1 ON l.id = dl1.domain_id AND dl1.property_code = 'OA5'
            LEFT JOIN model.entity d1 ON dl1.range_id = d1.id
            LEFT JOIN model.link_property dl2 ON l.id = dl2.domain_id AND dl2.property_code = 'OA6'
            LEFT JOIN model.entity d2 ON dl2.range_id = d2.id
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
        sql = """
            DELETE FROM model.link
            WHERE property_code IN %(codes)s AND (domain_id = %(id)s OR range_id = %(id)s);"""
        g.cursor.execute(sql, {'id': entity.id, 'codes': tuple(codes)})
        debug_model['link sql'] += 1

    @staticmethod
    def get_by_id(id_):
        sql = """
            SELECT l.id, l.property_code, l.domain_id, l.range_id, l.description, l.created,
                l.modified,
                min(date_part('year', d1.value_timestamp)) AS first,
                max(date_part('year', d2.value_timestamp)) AS last,
                (SELECT t.id FROM model.entity t
                    JOIN model.link_property lp ON t.id = lp.range_id
                        AND lp.domain_id = l.id
                        And lp.property_code = 'P2'
                ) AS type_id
            FROM model.link l
            LEFT JOIN model.link_property dl1 ON l.id = dl1.domain_id AND dl1.property_code = 'OA5'
            LEFT JOIN model.entity d1 ON dl1.range_id = d1.id
            LEFT JOIN model.link_property dl2 ON l.id = dl2.domain_id AND dl2.property_code = 'OA6'
            LEFT JOIN model.entity d2 ON dl2.range_id = d2.id
            WHERE l.id = %(id)s GROUP BY l.id;"""
        g.cursor.execute(sql, {'id': id_})
        debug_model['link sql'] += 1
        return Link(g.cursor.fetchone())

    @staticmethod
    def delete(id_):
        from openatlas.util.util import is_authorized
        if not is_authorized('editor'):  # pragma: no cover
            abort(403)
        g.cursor.execute("DELETE FROM model.link WHERE id = %(id)s;", {'id': id_})
        debug_model['link sql'] += 1

    @staticmethod
    def update(link):
        sql = """UPDATE model.link SET (property_code, domain_id, range_id, description) =
            (%(property_code)s, %(domain_id)s, %(range_id)s, %(description)s) WHERE id = %(id)s;"""
        g.cursor.execute(sql, {
            'id': link.id,
            'property_code': link.property.code,
            'domain_id': link.domain.id,
            'range_id': link.range.id,
            'description': link.description})
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
                    WHERE
                        l.property_code = %(property)s AND
                        d.class_code = %(domain)s AND
                        r.class_code = %(range)s;"""
                g.cursor.execute(sql, {
                    'property': item['property'],
                    'domain': item['domain'],
                    'range': item['range']})
                debug_model['link sql'] += 1
                for row2 in g.cursor.fetchall():
                    domain = EntityMapper.get_by_id(row2.domain_id)
                    range_ = EntityMapper.get_by_id(row2.range_id)
                    invalid_links.append({
                        'domain': link(domain) + ' (' + domain.class_.code + ')',
                        'property': link(g.properties[row2.property_code]),
                        'range': link(range_) + ' (' + range_.class_.code + ')'})
        return invalid_links
