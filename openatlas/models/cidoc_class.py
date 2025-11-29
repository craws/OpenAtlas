from __future__ import annotations

from dataclasses import dataclass, field

from flask import g

from openatlas import app
from openatlas.database import cidoc_class as db


@dataclass
class CidocClass:
    name: str
    code: str
    comment: str
    count: int = 0
    i18n: dict[str, str] = field(default_factory=lambda: {})
    sub: list[CidocClass] = field(default_factory=lambda: [])
    super: list[CidocClass] = field(default_factory=lambda: [])


def get_cidoc_classes(
        language: str,
        with_count: bool = False) -> dict[str, CidocClass]:
    classes = {
        row['code']: CidocClass(**row) for row in db.get_classes(with_count)}
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
