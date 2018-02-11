# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import g

import openatlas


class LinkPropertyMapper:

    @staticmethod
    def insert(link, property_code, range_):
        sql = """
            INSERT INTO model.link_property (property_code, domain_id, range_id)
            VALUES (%(property_code)s, %(domain_id)s, %(range_id)s);"""
        g.cursor.execute(sql, {
            'property_code': property_code,
            'domain_id': link if isinstance(link, int) else link.id,
            'range_id': range_ if isinstance(range_, int) else range_.id})
        openatlas.debug_model['div sql'] += 1

    @staticmethod
    def get_entities_by_node(node):
        sql = """
            SELECT l.domain_id, l.range_id
            FROM model.link l
            JOIN model.link_property lp ON l.id = lp.domain_id AND lp.range_id = %(node_id)s;"""
        g.cursor.execute(sql, {'node_id': node if isinstance(node, int) else node.id})
        openatlas.debug_model['div sql'] += 1
        return g.cursor.fetchall()
