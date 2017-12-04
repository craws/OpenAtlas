# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
import openatlas
from openatlas.models.link import Link


class LinkPropertyMapper(object):

    @staticmethod
    def insert(link, property_code, range_):
        if not link or not range_:
            return
        link_id = link.id if type(link) is Link else int(link)
        range_id = range_.id if type(range_) is openatlas.Entity else int(range_)
        sql = """
            INSERT INTO model.link_property (property_code, domain_id, range_id)
            VALUES (%(property_code)s, %(domain_id)s, %(range_id)s);"""
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {
            'property_code': property_code,
            'domain_id': link_id,
            'range_id': range_id})
