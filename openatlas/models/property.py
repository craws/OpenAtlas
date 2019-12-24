from dataclasses import dataclass
from typing import Dict, List

from flask import g, session

import openatlas
from openatlas import app


@dataclass
class Property:

    _name: str
    _name_inverse: str
    comment: str
    code: str
    id: int
    i18n: Dict[str, str]
    i18n_inverse: Dict[str, str]
    sub: List[int]
    super: List[int]
    domain_class_code: str
    range_class_code: str

    @property
    def name(self) -> str:
        locale_session = openatlas.get_locale()
        if locale_session in self.i18n:
            return self.i18n[locale_session]
        locale_default = session['settings']['default_language']
        if locale_default in self.i18n:
            return self.i18n[locale_default]
        return getattr(self, '_name')  # pragma: no cover

    @property
    def name_inverse(self) -> str:
        locale_session = openatlas.get_locale()
        if locale_session in self.i18n_inverse:
            return self.i18n_inverse[locale_session]
        locale_default = session['settings']['default_language']
        if locale_default in self.i18n_inverse:
            return self.i18n_inverse[locale_default]
        return getattr(self, '_name_inverse')  # pragma: no cover

    def find_object(self, attr: str, class_id: int) -> bool:
        # Used to check if links are CIDOC CRM valid
        valid_domain_id = getattr(self, attr)
        if valid_domain_id == class_id:
            return True
        return self.find_subs(attr, class_id, g.classes[valid_domain_id].sub)

    def find_subs(self, attr: str, class_id: int, valid_subs: List[int]) -> bool:
        for sub_id in valid_subs:
            if sub_id == class_id:
                return True
            elif self.find_subs(attr, class_id, g.classes[sub_id].sub):
                return True
        return False


class PropertyMapper:

    @staticmethod
    def get_all() -> Dict[str, Property]:
        sql = """
            SELECT id, code, comment, domain_class_code, range_class_code, name, name_inverse
            FROM model.property;"""
        g.execute(sql)
        properties = {row.code: Property(id=row.id,
                                         _name=row.name,
                                         _name_inverse=row.name_inverse,
                                         code=row.code,
                                         comment=row.comment,
                                         domain_class_code=row.domain_class_code,
                                         range_class_code=row.range_class_code,
                                         sub=[], super=[], i18n={}, i18n_inverse={}
                                         ) for row in g.cursor.fetchall()}
        g.execute('SELECT super_code, sub_code FROM model.property_inheritance;')
        for row in g.cursor.fetchall():
            properties[row.super_code].sub.append(row.sub_code)
            properties[row.sub_code].super.append(row.super_code)
        sql = """
            SELECT property_code, language_code, text, text_inverse FROM model.property_i18n
            WHERE language_code IN %(language_codes)s;"""
        g.execute(sql, {'language_codes': tuple(app.config['LANGUAGES'].keys())})
        for row in g.cursor.fetchall():
            property_ = properties[row.property_code]
            if row.language_code not in property_.i18n:
                property_.i18n[row.language_code] = {}
            property_.i18n[row.language_code] = row.text
            if row.language_code not in property_.i18n_inverse:
                property_.i18n_inverse[row.language_code] = {}
            property_.i18n_inverse[row.language_code] = row.text_inverse
        return properties
