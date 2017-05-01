# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import session
import openatlas


class Property(object):

    def __init__(self, row):
        self._comment = ''
        self._name = row.name
        self._name_inverse = row.name_inverse
        self.code = row.code
        self.domain_id = row.domain_class_id
        self.id = row.id
        self.i18n = {}
        self.range_id = row.range_class_id
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
        return self.find_subs(attr, class_id, openatlas.classes[valid_domain_id].sub)

    def find_subs(self, attr, class_id, valid_subs):
        for sub_id in valid_subs:
            if sub_id == class_id:
                return True
            elif self.find_subs(attr, class_id, openatlas.classes[sub_id].sub):
                return True


class PropertyMapper(object):

    @staticmethod
    def get_all():
        properties = {}
        cursor = openatlas.get_cursor()
        cursor.execute("SELECT id, code, domain_class_id, range_class_id, name, name_inverse FROM model.property;")
        for row in cursor.fetchall():
            properties[row.id] = Property(row)
        cursor.execute('SELECT super_id, sub_id FROM model.property_inheritance;')
        for row in cursor.fetchall():
            properties[row.super_id].sub.append(row.sub_id)
            properties[row.sub_id].super.append(row.super_id)
        sql = """SELECT text, language_code, table_field, table_id FROM model.i18n
                WHERE table_name = 'property' AND language_code IN %(language_codes)s;"""
        cursor.execute(sql, {'language_codes': tuple(openatlas.app.config['LANGUAGES'].keys())})
        for row in cursor.fetchall():
            if row.language_code not in properties[row.table_id].i18n:
                properties[row.table_id].i18n[row.language_code] = {}
            properties[row.table_id].i18n[row.language_code][row.table_field] = row.text
        return properties

    @staticmethod
    def get_by_code(code):
        for id_ in openatlas.properties:
            if openatlas.properties[id_].code == code:
                return openatlas.properties[id_]
