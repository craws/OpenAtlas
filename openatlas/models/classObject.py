from flask import g, session

import openatlas
from openatlas import app
from dataclasses import dataclass


@dataclass
class ClassObject:

    _name: str
    code: str
    id: int
    i18n: dict
    sub: list
    super: list
    _comment: str = ''

    @property
    def name(self) -> str:
        return self.get_i18n('name')

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
        return getattr(self, '_' + attribute)  # pragma: no cover


class ClassMapper:

    @staticmethod
    def get_all() -> dict:
        g.execute("SELECT id, code, name FROM model.class;")
        classes = {row.code: ClassObject(_name=row.name, code=row.code, id=row.id, i18n={},
                                         sub=[], super=[]) for row in g.cursor.fetchall()}
        g.execute("SELECT super_code, sub_code FROM model.class_inheritance;")
        for row in g.cursor.fetchall():
            classes[row.super_code].sub.append(row.sub_code)
            classes[row.sub_code].super.append(row.super_code)
        sql = """
            SELECT class_code, language_code, attribute, text FROM model.class_i18n
            WHERE language_code IN %(language_codes)s;"""
        g.execute(sql, {'language_codes': tuple(app.config['LANGUAGES'].keys())})
        for row in g.cursor.fetchall():
            class_ = classes[row.class_code]
            if row.language_code not in class_.i18n:
                class_.i18n[row.language_code] = {}
            class_.i18n[row.language_code][row.attribute] = row.text
        return classes
