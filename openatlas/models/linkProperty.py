# Created by Alexander Watzinger and others. Please see README.md for licensing information
from flask import g

from openatlas import debug_model


class LinkPropertyMapper:

    @staticmethod
    def insert(link, property_code, range_):
        sql = """
            INSERT INTO model.link_property (property_code, domain_id, range_id)
            VALUES (%(property_code)s, %(domain_id)s, %(range_id)s);"""
        g.cursor.execute(sql, {
            'property_code': property_code,
            'domain_id': link if type(link) is int else link.id,
            'range_id': range_ if type(range_) is int else range_.id})
        debug_model['link sql'] += 1

    @staticmethod
    def get_entities_by_node(node):
        sql = """
            SELECT l.id, l.domain_id, l.range_id FROM model.link l
            JOIN model.link_property lp ON l.id = lp.domain_id AND lp.range_id = %(node_id)s;"""
        g.cursor.execute(sql, {'node_id': node if type(node) is int else node.id})
        debug_model['link sql'] += 1
        return g.cursor.fetchall()
