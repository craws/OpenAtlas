# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import openatlas


class Link(object):

    def __init__(self, row):
        self.id = row.id
        self.property = openatlas.properties[row.property_id]
        self.domain = openatlas.EntityMapper.get_by_id(row.domain_id)
        self.range = openatlas.EntityMapper.get_by_id(row.range_id)


class LinkMapper(object):

    @staticmethod
    def insert(domain, property_code, range_):
        if not domain or not range_:
            return
        range_ = range_ if isinstance(range_, list) else [range_]
        for range_param in range_:
            if not range_param:
                continue
            domain_id = domain.id if type(domain) is openatlas.Entity else int(domain)
            range_id = range_param.id if type(range_param) is openatlas.Entity else int(range_param)
            sql = """
                INSERT INTO model.link (property_id, domain_id, range_id)
                VALUES ((
                    SELECT id FROM model.property
                    WHERE code = %(property_code)s), %(domain_id)s, %(range_id)s);"""
            # Todo: build only sql and get execution out of loop
            cursor = openatlas.get_cursor()
            cursor.execute(sql, {
                'property_code': property_code,
                'domain_id': domain_id,
                'range_id': range_id})
            openatlas.debug_model['div sql'] += 1

    @staticmethod
    def get_linked_entities(entity, codes, inverse=False):
        codes = codes if isinstance(codes, list) else [codes]
        cursor = openatlas.get_cursor()
        sql = """
            SELECT l.range_id AS result_id
            FROM model.link l
            JOIN model.property p ON l.property_id = p.id AND p.code IN %(codes)s
            WHERE domain_id = %(entity_id)s;"""
        if inverse:
            sql = """
                SELECT domain_id AS result_id
                FROM model.link
                WHERE range_id = %(entity_id)s AND property_id IN %(property_ids)s;"""
        cursor.execute(sql, {'entity_id': entity.id, 'codes': tuple(codes)})
        openatlas.debug_model['div sql'] += 1
        ids = [element for (element,) in cursor.fetchall()]
        return openatlas.EntityMapper.get_by_ids(ids)
