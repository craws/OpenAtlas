from __future__ import annotations

from typing import Any

from flask import g

from openatlas import app
from openatlas.database import cidoc_class as db


class CidocClass:

    def __init__(self, data: dict[str, Any]) -> None:
        self.name = data['name']
        self.code = data['code']
        self.id = data['id']
        self.comment = data['comment']
        self.count = data['count']
        self.i18n: dict[str, str] = {}
        self.sub: list[CidocClass] = []
        self.super: list[CidocClass] = []

    @staticmethod
    def get_all(language: str) -> dict[str, CidocClass]:
        classes = {row['code']: CidocClass(row) for row in db.get_classes()}
        for row in db.get_hierarchy():
            classes[row['super_code']].sub.append(row['sub_code'])
            classes[row['sub_code']].super.append(row['super_code'])
        for row in db.get_translations(app.config['LANGUAGES']):
            classes[row['class_code']].i18n[row['language_code']] = row['text']
        for class_ in classes.values():
            if language in class_.i18n:
                class_.name = class_.i18n[language]
            elif g.settings['default_language'] in class_.i18n:
                class_.name = class_.i18n[g.settings['default_language']]
        return classes
