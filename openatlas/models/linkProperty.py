# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import openatlas
from openatlas.models.link import Link


class LinkPropertyMapper(object):

    @staticmethod
    def insert(link, property_code, range_):
        if not link or not range_:
            return
        link_id = link.id if isinstance(link, Link) else int(link)
        range_id = range_.id if isinstance(range_, openatlas.Entity) else int(range_)
        sql = """
            INSERT INTO model.link_property (property_code, domain_id, range_id)
            VALUES (%(property_code)s, %(domain_id)s, %(range_id)s);"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {
            'property_code': property_code,
            'domain_id': link_id,
            'range_id': range_id})
        openatlas.debug_model['div sql'] += 1

    @staticmethod
    def get_entities_by_node(node):
        from openatlas.models.entity import Entity
        node_id = node.id if isinstance(node, Entity) else int(node)
        sql = """
            SELECT l.domain_id, l.range_id
            FROM model.link l
            JOIN model.link_property lp ON l.id = lp.domain_id AND lp.range_id = %(node_id)s;"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {'node_id': node_id})
        openatlas.debug_model['div sql'] += 1
        return cursor.fetchall()
