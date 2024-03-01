from __future__ import annotations

from typing import Any

from flask import g

from openatlas import app
from openatlas.database import cidoc_property as db


class CidocProperty:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data['id']
        self.name = data['name']
        self.name_inverse = data['name_inverse']
        self.code = data['code']
        self.comment = data['comment']
        self.domain_class_code = data['domain_class_code']
        self.range_class_code = data['range_class_code']
        self.count = data['count']
        self.sub: list[int] = []
        self.super: list[int] = []
        self.i18n: dict[str, str] = {}
        self.i18n_inverse: dict[str, str] = {}

    def find_object(self, attr: str, class_id: int) -> bool:
        valid_domain_id = getattr(self, attr)
        if valid_domain_id == class_id:
            return True
        return self.find_subs(
            attr,
            class_id,
            g.cidoc_classes[valid_domain_id].sub)

    def find_subs(
            self,
            attr: str,
            class_id: int,
            valid_subs: list[int]) -> bool:
        for sub_id in valid_subs:
            if sub_id == class_id or \
                    self.find_subs(
                        attr,
                        class_id,
                        g.cidoc_classes[sub_id].sub):
                return True
        return False

    @staticmethod
    def get_all(language: str) -> dict[str, CidocProperty]:
        properties = {
            row['code']: CidocProperty(row) for row in db.get_properties()}
        for row in db.get_hierarchy():
            properties[row['super_code']].sub.append(row['sub_code'])
            properties[row['sub_code']].super.append(row['super_code'])
        for row in db.get_translations(app.config['LANGUAGES']):
            properties[row['property_code']].i18n[row['language_code']] = \
                row['text']
            properties[row['property_code']].i18n_inverse[
                row['language_code']] = row['text_inverse']
        for property_ in properties.values():
            default = g.settings['default_language']
            if language in property_.i18n:
                property_.name = property_.i18n[language]
            elif default in property_.i18n:
                property_.name = property_.i18n[default]
            if language in property_.i18n_inverse:
                property_.name_inverse = property_.i18n_inverse[language]
            elif default in property_.i18n_inverse:
                property_.name_inverse = property_.i18n_inverse[default]
        return properties
