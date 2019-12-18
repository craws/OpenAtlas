from __future__ import annotations  # Needed for Python 4.0 type annotations

from dataclasses import dataclass
from typing import Dict, List

from flask import g, session

import openatlas
from openatlas import app


@dataclass
class ClassObject:

    _name: str
    comment: str
    code: str
    id: int
    i18n: Dict[str, str]
    sub: List[ClassObject]
    super: List[ClassObject]

    @property
    def name(self) -> str:
        return self.get_i18n()

    def get_i18n(self) -> str:
        locale_session = openatlas.get_locale()
        if locale_session in self.i18n:
            return self.i18n[locale_session]
        locale_default = session['settings']['default_language']
        if locale_default in self.i18n:
            return self.i18n[locale_default]
        return getattr(self, '_name')  # pragma: no cover


class ClassMapper:

    @staticmethod
    def get_all() -> Dict[str, ClassObject]:
        g.execute("SELECT id, code, name, comment FROM model.class;")
        classes: Dict[str, ClassObject] = {
            row.code: ClassObject(_name=row.name, code=row.code, id=row.id, comment=row.comment,
                                  i18n={}, sub=[], super=[]) for row in g.cursor.fetchall()}
        g.execute("SELECT super_code, sub_code FROM model.class_inheritance;")
        for row in g.cursor.fetchall():
            classes[row.super_code].sub.append(row.sub_code)
            classes[row.sub_code].super.append(row.super_code)
        sql = """
            SELECT class_code, language_code, text FROM model.class_i18n
            WHERE language_code IN %(language_codes)s;"""
        g.execute(sql, {'language_codes': tuple(app.config['LANGUAGES'].keys())})
        for row in g.cursor.fetchall():
            classes[row.class_code].i18n[row.language_code] = row.text
        return classes
