# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import flash, session
from flask_babel import lazy_gettext as _

import openatlas


class Link(object):

    def __init__(self, row):
        self.id = row.id
        self.description = row.description
        self.property = openatlas.properties[row.property_id]
        # Todo: performance - if it's a node don't call get_by_id
        self.domain = openatlas.EntityMapper.get_by_id(row.domain_id)
        self.range = openatlas.EntityMapper.get_by_id(row.range_id)

    def update(self):
        LinkMapper.update(self)


class LinkMapper(object):

    @staticmethod
    def insert(domain, property_code, range_, description=None):
        if not domain or not range_:
            return
        range_ = range_ if isinstance(range_, list) else [range_]
        result = None
        for range_param in range_:
            if not range_param:
                continue
            domain_id = domain.id if type(domain) is openatlas.Entity else int(domain)
            range_id = range_param.id if type(range_param) is openatlas.Entity else int(range_param)
            if 'settings' in session and session['settings']['debug_mode']:  # pragma: no cover
                domain = domain if type(
                    domain) is openatlas.Entity else openatlas.EntityMapper.get_by_id(int(domain))
                range_ = range_param if type(
                    range_param) is openatlas.Entity else openatlas.EntityMapper.get_by_id(
                    int(range_param))
                domain_class = openatlas.classes[domain.class_.id]
                range_class = openatlas.classes[range_.class_.id]
                property_ = openatlas.PropertyMapper.get_by_code(property_code)
                ignore = openatlas.app.config['WHITELISTED_DOMAINS']
                domain_error = True
                if property_.find_object('domain_id', domain_class.id):
                    domain_error = False
                if domain_class.code in ignore:
                    domain_error = False
                range_error = False if property_.find_object('range_id', range_class.id) else True
                if domain_error or range_error:
                    text = _('error link') + ': ' + domain_class.name + ' > '
                    text += property_code + ' > ' + range_class.name
                    flash(text, 'error')
                    continue
            sql = """
                INSERT INTO model.link (property_id, domain_id, range_id, description)
                VALUES (
                    (SELECT id FROM model.property WHERE code = %(property_code)s),
                    %(domain_id)s,
                    %(range_id)s,
                    %(description)s)
                RETURNING id;"""
            # Todo: build only sql and get execution out of loop
            cursor = openatlas.get_cursor()
            cursor.execute(sql, {
                'property_code': property_code,
                'domain_id': domain_id,
                'range_id': range_id,
                'description': description})
            openatlas.debug_model['div sql'] += 1
            result = cursor.fetchone()[0]
        return result

    @staticmethod
    def get_linked_entity(entity, code, inverse=False):
        result = LinkMapper.get_linked_entities(entity, code, inverse)
        if len(result) > 1:
            # Todo: log this error
            flash('alert multiple linked entities found', 'error')
            return result[0]  # return first one nevertheless to not bring the application down
        if result:
            return result[0]

    @staticmethod
    def get_linked_entities(entity, codes, inverse=False):
        codes = codes if isinstance(codes, list) else [codes]
        sql = """
            SELECT l.range_id AS result_id
            FROM model.link l
            JOIN model.property p ON l.property_id = p.id AND p.code IN %(codes)s
            WHERE domain_id = %(entity_id)s;"""
        if inverse:
            sql = """
                SELECT l.domain_id AS result_id
                FROM model.link l
                JOIN model.property p ON l.property_id = p.id AND p.code IN %(codes)s
                WHERE l.range_id = %(entity_id)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'entity_id': entity.id, 'codes': tuple(codes)})
        openatlas.debug_model['div sql'] += 1
        ids = [element for (element,) in cursor.fetchall()]
        return openatlas.EntityMapper.get_by_ids(ids)

    @staticmethod
    def get_links(entity, codes, inverse=False):
        codes = codes if isinstance(codes, list) else [codes]
        entity_id = entity.id if type(entity) is openatlas.Entity else int(entity)
        first = 'range' if inverse else 'domain'
        second = 'domain' if inverse else 'range'
        sql = """
            SELECT l.id, l.property_id, l.domain_id, l.range_id, l.description, l.created,
                l.modified, e.name,
                min(date_part('year', d1.value_timestamp)) AS first,
                max(date_part('year', d2.value_timestamp)) AS last,
                (SELECT t.id FROM model.entity t
                    JOIN model.link_property lp ON t.id = lp.range_id AND lp.domain_id = l.id
                    WHERE lp.property_id = (SELECT id FROM model.property WHERE code = 'P2')
                ) AS type_id

            FROM model.link l
            JOIN model.entity e ON l.{second}_id = e.id
            JOIN model.property p ON l.property_id = p.id AND p.code IN %(codes)s

            LEFT JOIN model.link_property dl1 ON l.id = dl1.domain_id AND
                dl1.property_id IN (SELECT id FROM model.property WHERE code = 'OA5')
            LEFT JOIN model.entity d1 ON dl1.range_id = d1.id

            LEFT JOIN model.link_property dl2 ON l.id = dl2.domain_id
                AND dl2.property_id IN (SELECT id FROM model.property WHERE code = 'OA6')
            LEFT JOIN model.entity d2 ON dl2.range_id = d2.id

            WHERE l.{first}_id = %(entity_id)s GROUP BY l.id, e.name ORDER BY e.name;""".format(
            first=first, second=second)
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'entity_id': entity_id, 'codes': tuple(codes)})
        openatlas.debug_model['div sql'] += 1
        links = []
        for row in cursor.fetchall():
            links.append(Link(row))
        return links

    @staticmethod
    def delete_by_codes(entity, codes):
        from openatlas import PropertyMapper
        codes = codes if isinstance(codes, list) else [codes]
        property_ids = []
        for code in codes:
            property_ids.append(PropertyMapper.get_by_code(code).id)
        sql = "DELETE FROM model.link WHERE domain_id = %(id)s AND property_id IN %(property_ids)s;"
        openatlas.get_cursor().execute(sql, {'id': entity.id, 'property_ids': tuple(property_ids)})

    @staticmethod
    def get_by_id(id_):
        sql = """
            SELECT l.id, l.property_id, l.domain_id, l.range_id, l.description, l.created,
                l.modified,
                min(date_part('year', d1.value_timestamp)) AS first,
                max(date_part('year', d2.value_timestamp)) AS last,
                (SELECT t.id FROM model.entity t
                    JOIN model.link_property lp ON t.id = lp.range_id AND lp.domain_id = l.id
                    WHERE lp.property_id = (SELECT id FROM model.property WHERE code = 'P2')
                ) AS type_id

            FROM model.link l

            LEFT JOIN model.link_property dl1 ON l.id = dl1.domain_id AND
                dl1.property_id IN (SELECT id FROM model.property WHERE code = 'OA5')
            LEFT JOIN model.entity d1 ON dl1.range_id = d1.id
            LEFT JOIN model.link_property dl2 ON l.id = dl2.domain_id
                AND dl2.property_id IN (SELECT id FROM model.property WHERE code = 'OA6')
            LEFT JOIN model.entity d2 ON dl2.range_id = d2.id

            WHERE l.id = %(id)s GROUP BY l.id;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'id': id_})
        openatlas.debug_model['div sql'] += 1
        return Link(cursor.fetchone())

    @staticmethod
    def delete_by_id(id_):
        openatlas.get_cursor().execute("DELETE FROM model.link WHERE id = %(id)s;", {'id': id_})

    @staticmethod
    def update(link):
        sql = """UPDATE model.link SET (property_id, domain_id, range_id, description) =
            (%(property_id)s, %(domain_id)s, %(range_id)s, %(description)s) WHERE id = %(id)s;"""
        openatlas.get_cursor().execute(sql, {
            'id': link.id,
            'property_id': link.property.id,
            'domain_id': link.domain.id,
            'range_id': link.range.id,
            'description': link.description})
        openatlas.debug_model['div sql'] += 1
