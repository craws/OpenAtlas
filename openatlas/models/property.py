# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Dict

from flask import g, session

import openatlas
from openatlas import app


class Property:

    def __init__(self, row) -> None:
        self._comment = ''
        self._name = row.name
        self._name_inverse = row.name_inverse
        self.code = row.code
        self.domain_class_code = row.domain_class_code
        self.range_class_code = row.range_class_code
        self.id = row.id
        self.i18n: dict = {}
        self.super: list = []
        self.sub: list = []

    @property
    def name(self) -> str:
        return self.get_i18n('name')

    @property
    def name_inverse(self) -> str:
        return self.get_i18n('name_inverse')

    @property
    def comment(self) -> str:
        return self.get_i18n('comment')

    def get_i18n(self, attribute: str) -> str:
        locale_session = openatlas.get_locale()
        if locale_session in self.i18n and attribute in self.i18n[locale_session]:
            return self.i18n[locale_session][attribute]
        locale_default = session['settings']['default_language']
        if locale_default in self.i18n and attribute in self.i18n[locale_default]:
            return self.i18n[locale_default][attribute]
        return getattr(self, '_' + attribute)

    def find_object(self, attr: str, class_id: int) -> bool:
        # Used to check if links are CIDOC CRM valid
        valid_domain_id = getattr(self, attr)
        if valid_domain_id == class_id:
            return True
        return self.find_subs(attr, class_id, g.classes[valid_domain_id].sub)

    def find_subs(self, attr: str, class_id: int, valid_subs: list) -> bool:
        for sub_id in valid_subs:
            if sub_id == class_id:
                return True
            elif self.find_subs(attr, class_id, g.classes[sub_id].sub):
                return True
        return False


class PropertyMapper:

    @staticmethod
    def get_all() -> Dict:
        sql = """
            SELECT id, code, domain_class_code, range_class_code, name, name_inverse
            FROM model.property;"""
        g.execute(sql)
        properties = {row.code: Property(row) for row in g.cursor.fetchall()}
        g.execute('SELECT super_code, sub_code FROM model.property_inheritance;')
        for row in g.cursor.fetchall():
            properties[row.super_code].sub.append(row.sub_code)
            properties[row.sub_code].super.append(row.super_code)
        sql = """
            SELECT property_code, language_code, attribute, text FROM model.property_i18n
            WHERE language_code IN %(language_codes)s;"""
        g.execute(sql, {'language_codes': tuple(app.config['LANGUAGES'].keys())})
        for row in g.cursor.fetchall():
            property_ = properties[row.property_code]
            if row.language_code not in property_.i18n:
                property_.i18n[row.language_code] = {}
            property_.i18n[row.language_code][row.attribute] = row.text
        return properties
