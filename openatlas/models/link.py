# Created 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import abort, flash, g, session
from flask_babel import lazy_gettext as _

from openatlas import app, debug_model, logger


class Link:

    def __init__(self, row):
        from openatlas.models.entity import EntityMapper
        self.id = row.id
        self.description = row.description
        self.property = g.properties[row.property_code]
        # Todo: performance - if it's a node don't call get_by_id
        self.domain = EntityMapper.get_by_id(row.domain_id)
        self.range = EntityMapper.get_by_id(row.range_id)
        self.type = g.nodes[row.type_id] if row.type_id else None
        self.first = int(row.first) if hasattr(row, 'first') and row.first else None
        self.last = int(row.last) if hasattr(row, 'last') and row.last else None
        self.dates = {}

    def update(self):
        LinkMapper.update(self)

    def delete(self):
        LinkMapper.delete_by_id(self.id)

    def set_dates(self):
        from openatlas.models.date import DateMapper
        self.dates = DateMapper.get_link_dates(self)


class LinkMapper:

    @staticmethod
    def insert(domain, property_code, range_, description=None):
        if not domain or not range_:
            return
        range_ = range_ if isinstance(range_, list) else [range_]
        result = None
        for range_ in range_:
            domain_id = domain if isinstance(domain, int) else domain.id
            range_id = range_ if isinstance(range_, int) else range_.id
            if 'settings' in session and session['settings']['debug_mode']:  # pragma: no cover
                from openatlas.models.entity import EntityMapper
                domain = domain if not isinstance(domain, int) else EntityMapper.get_by_id(domain)
                range_ = range_ if not isinstance(range_, int) else EntityMapper.get_by_id(range_)
                domain_class = g.classes[domain.class_.code]
                range_class = g.classes[range_.class_.code]
                property_ = g.properties[property_code]
                ignore = app.config['WHITELISTED_DOMAINS']
                domain_error = True
                range_error = True
                if property_.find_object('domain_class_code', domain_class.code):
                    domain_error = False
                if domain_class.code in ignore:
                    domain_error = False
                if property_.find_object('range_class_code', range_class.code):
                    range_error = False
                if domain_error or range_error:
                    text = _('error link') + ': ' + domain_class.name + ' > '
                    text += property_code + ' > ' + range_class.name
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
                'domain_id': domain_id,
                'range_id': range_id,
                'description': description})
            debug_model['div sql'] += 1
            result = g.cursor.fetchone()[0]
        return result

    @staticmethod
    def get_linked_entity(entity_param, code, inverse=False):
        result = LinkMapper.get_linked_entities(entity_param, code, inverse)
        if len(result) > 1:  # pragma: no cover
            message = 'multiple linked entities found for ' + code
            logger.log('error', 'model', message)
            flash(_('error multiple linked entities found'), 'error')
            return result[0]  # return first one nevertheless
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
            'entity_id': entity if isinstance(entity, int) else entity.id,
            'codes': tuple(codes if isinstance(codes, list) else [codes])})
        debug_model['div sql'] += 1
        ids = [element for (element,) in g.cursor.fetchall()]
        return EntityMapper.get_by_ids(ids)

    @staticmethod
    def get_links(entity, codes, inverse=False):
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
            'entity_id': entity if isinstance(entity, int) else entity.id,
            'codes': tuple(codes if isinstance(codes, list) else [codes])})
        debug_model['div sql'] += 1
        links = []
        for row in g.cursor.fetchall():
            links.append(Link(row))
        return links

    @staticmethod
    def delete_by_codes(entity, codes):
        codes = codes if isinstance(codes, list) else [codes]
        sql = "DELETE FROM model.link WHERE domain_id = %(id)s AND property_code IN %(codes)s;"
        g.cursor.execute(sql, {'id': entity.id, 'codes': tuple(codes)})

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
        debug_model['div sql'] += 1
        return Link(g.cursor.fetchone())

    @staticmethod
    def delete_by_id(id_):
        from openatlas.util.util import is_authorized
        if not is_authorized('editor'):  # pragma: no cover
            abort(403)
        g.cursor.execute("DELETE FROM model.link WHERE id = %(id)s;", {'id': id_})

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
        debug_model['div sql'] += 1
