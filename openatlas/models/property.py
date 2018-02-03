# Copyright 2017 by Alexander Watzinger and others. Please see README.md for licensing information
from flask import session, g

import openatlas
from openatlas import app


class Property:

    def __init__(self, row):
        self._comment = ''
        self._name = row.name
        self._name_inverse = row.name_inverse
        self.code = row.code
        self.domain_class_code = row.domain_class_code
        self.id = row.id
        self.i18n = {}
        self.range_class_code = row.range_class_code
        self.super = []
        self.sub = []

    @property
    def name(self):
        return self.get_i18n('name')

    @property
    def name_inverse(self):
        return self.get_i18n('name_inverse')

    @property
    def comment(self):
        return self.get_i18n('comment')

    def get_i18n(self, attribute):
        locale_session = openatlas.get_locale()
        locale_default = session['settings']['default_language']
        if locale_session in self.i18n and attribute in self.i18n[locale_session]:
            return self.i18n[locale_session][attribute]
        elif locale_default in self.i18n and attribute in self.i18n[locale_default]:
            return self.i18n[locale_default][attribute]
        return getattr(self, '_' + attribute)

    def find_object(self, attr, class_id):
        valid_domain_id = getattr(self, attr)
        if valid_domain_id == class_id:
            return True
        return self.find_subs(attr, class_id, g.classes[valid_domain_id].sub)

    def find_subs(self, attr, class_id, valid_subs):
        for sub_id in valid_subs:
            if sub_id == class_id:
                return True
            elif self.find_subs(attr, class_id, g.classes[sub_id].sub):
                return True


class PropertyMapper:

    @staticmethod
    def get_all():
        properties = {}
        sql = """
            SELECT id, code, domain_class_code, range_class_code, name, name_inverse
            FROM model.property;"""
        g.cursor.execute(sql)
        for row in g.cursor.fetchall():
            properties[row.code] = Property(row)
        g.cursor.execute('SELECT super_code, sub_code FROM model.property_inheritance;')
        for row in g.cursor.fetchall():
            properties[row.super_code].sub.append(row.sub_code)
            properties[row.sub_code].super.append(row.super_code)
        sql = """
            SELECT property_code, language_code, attribute, text FROM model.property_i18n
            WHERE language_code IN %(language_codes)s;"""
        g.cursor.execute(sql, {'language_codes': tuple(app.config['LANGUAGES'].keys())})
        for row in g.cursor.fetchall():
            property_ = properties[row.property_code]
            if row.language_code not in property_.i18n:
                property_.i18n[row.language_code] = {}
            property_.i18n[row.language_code][row.attribute] = row.text
        return properties
