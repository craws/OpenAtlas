# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import session

import openatlas


class Property(object):
    code = None
    comment_translated = None
    domain_id = None
    name = None
    name_inverse = None
    name_inverse_translated = None
    name_translated = None
    range_id = None
    super = []
    sub = []


class PropertyMapper(object):

    @staticmethod
    def get_all():
        sql = """SELECT p.id, p.code, p.domain_class_id, p.range_class_id, p.name, p.name_inverse, p.created, p.modified,
                COALESCE (
                  (SELECT text FROM model.i18n WHERE table_name = 'property' AND table_field = 'name' AND
                    table_id = p.id AND language_code = %(language_code)s),
                  (SELECT text FROM model.i18n WHERE table_name = 'property' AND table_field = 'name' AND
                    table_id = p.id AND language_code = %(language_default_code)s)
                ) as name_i18n,
                COALESCE (
                  (SELECT text FROM model.i18n WHERE table_name = 'property' AND table_field = 'name_inverse' AND
                    table_id = p.id AND language_code = %(language_code)s),
                  (SELECT text FROM model.i18n WHERE table_name = 'property' AND table_field = 'name_inverse' AND
                    table_id = p.id AND language_code = %(language_default_code)s)
                ) as name_inverse_i18n,
                COALESCE (
                  (SELECT text FROM model.i18n WHERE table_name = 'property' AND table_field = 'comment' AND
                    table_id = p.id AND language_code = %(language_code)s),
                  (SELECT text FROM model.i18n WHERE table_name = 'property' AND table_field = 'comment' AND
                    table_id = p.id AND language_code = %(language_default_code)s)
                ) as comment_i18n
                FROM model.property p"""
        properties = {}
        cursor = openatlas.get_cursor()
        cursor.execute(sql, {
            'language_code': openatlas.get_locale(),
            'language_default_code': session['settings']['default_language']
        })
        for row in cursor.fetchall():
            properties[row.id] = PropertyMapper.populate(row)
        cursor.execute('SELECT super_id, sub_id FROM model.property_inheritance;')
        for row in cursor.fetchall():
            properties[row.super_id].sub.append(row.sub_id)
            properties[row.sub_id].super.append(row.super_id)
        return properties

    @staticmethod
    def populate(row):
        object_ = Property()
        object_.id = row.id
        object_.domain_id = row.domain_class_id
        object_.range_id = row.range_class_id
        object_.name = row.name
        object_.created = row.created
        object_.modified = row.modified
        object_.code = row.code
        object_.name_translated = row.name_i18n
        object_.name_inverse = row.name_inverse
        object_.name_inverse_translated = row.name_inverse_i18n
        object_.comment_translated = row.comment_i18n
        return object_
