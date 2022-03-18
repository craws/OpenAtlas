from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any

from flask import g

from openatlas import app
from openatlas.database.cidoc_class import CidocClass as Db


class CidocClass:

    def __init__(self, data: dict[str, Any]) -> None:
        self._name = data['name']
        self.code = data['code']
        self.id = data['id']
        self.comment = data['comment']
        self.count = data['count']
        self.i18n: dict[str, str] = {}
        self.sub: list[CidocClass] = []
        self.super: list[CidocClass] = []

    @property
    def name(self) -> str:
        return self.get_i18n()

    def get_i18n(self) -> str:
        from openatlas import get_locale
        if get_locale() in self.i18n:
            return self.i18n[get_locale()]
        if g.settings['default_language'] in self.i18n:
            return self.i18n[g.settings['default_language']]
        return getattr(self, '_name')  # pragma: no cover

    @staticmethod
    def get_all() -> dict[str, CidocClass]:
        classes = {row['code']: CidocClass(row) for row in Db.get_classes()}
        for row in Db.get_hierarchy():
            classes[row['super_code']].sub.append(row['sub_code'])
            classes[row['sub_code']].super.append(row['super_code'])
        for row in Db.get_translations(app.config['LANGUAGES']):
            classes[row['class_code']].i18n[row['language_code']] = row['text']
        return classes
