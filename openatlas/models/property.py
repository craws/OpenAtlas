# Copyright 2017 by Alexander Watzinger and others. Please see the file README.md for licensing information
from flask import session
import openatlas


class Property(object):

    def __init__(self, row):
        self.code = row.code
        self.domain_id = row.domain_class_id
        self.id = row.id
        self.i18n = {}
        self.name = row.name
        self.name_inverse = row.name_inverse
        self.range_id = row.range_class_id
        self.super = []
        self.sub = []

    def get_i18n(self, attribute):
        locale_session = openatlas.get_locale()
        locale_default = session['settings']['default_language']
        if locale_session in self.i18n and attribute in self.i18n[locale_session]:
            return self.i18n[locale_session][attribute]
        elif locale_default in self.i18n and attribute in self.i18n[locale_default]:
            return self.i18n[locale_default][attribute]
        return self.name if attribute == 'name' else ''

    def find_object(self, attr, value):
        if getattr(self, attr) == value:
            return True
        else:
            for sub in self.sub:
                match = openatlas.properties[sub].find_object(attr, value)
                if match:
                    return True
        # return False


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
        sql = "SELECT text, language_code, table_field, table_id FROM model.i18n WHERE table_name = 'property';"
        cursor.execute(sql)
        for row in cursor.fetchall():
            property = properties[row.table_id]
            if row.language_code not in property.i18n:
                property.i18n[row.language_code] = {}
            property.i18n[row.language_code][row.table_field] = row.text
        return properties
