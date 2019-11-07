# Created by Alexander Watzinger and others. Please see README.md for licensing information
from typing import Dict

from flask import g, session

import openatlas
from openatlas import app


class ClassObject:

    def __init__(self, row) -> None:
        self._comment = ''
        self._name = row.name
        self.code = row.code
        self.id = row.id
        self.i18n: dict = {}
        self.sub: list = []
        self.super: list = []

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
        classes = {row.code: ClassObject(row) for row in g.cursor.fetchall()}
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
