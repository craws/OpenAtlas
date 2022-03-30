from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any

from flask import g

from openatlas import app
from openatlas.database.cidoc_property import CidocProperty as Db


class CidocProperty:

    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data['id']
        self._name = data['name']
        self._name_inverse = data['name_inverse']
        self.code = data['code']
        self.comment = data['comment']
        self.domain_class_code = data['domain_class_code']
        self.range_class_code = data['range_class_code']
        self.count = data['count']
        self.sub: list[int] = []
        self.super: list[int] = []
        self.i18n: dict[str, str] = {}
        self.i18n_inverse: dict[str, str] = {}

    @property
    def name(self) -> str:
        from openatlas import get_locale
        locale_session = get_locale()
        if locale_session in self.i18n:
            return self.i18n[locale_session]
        if g.settings['default_language'] in self.i18n:
            return self.i18n[g.settings['default_language']]
        return getattr(self, '_name')  # pragma: no cover

    @property
    def name_inverse(self) -> str:
        from openatlas import get_locale
        locale_session = get_locale()
        if locale_session in self.i18n_inverse:
            return self.i18n_inverse[locale_session]
        if g.settings['default_language'] in self.i18n_inverse:
            return self.i18n_inverse[g.settings['default_language']]
        return getattr(self, '_name_inverse')  # pragma: no cover

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
                    self.find_subs(attr, class_id, g.cidoc_classes[sub_id].sub):
                return True
        return False

    @staticmethod
    def get_all() -> dict[str, CidocProperty]:
        properties = {
            row['code']: CidocProperty(row) for row in Db.get_properties()}
        for row in Db.get_hierarchy():
            properties[row['super_code']].sub.append(row['sub_code'])
            properties[row['sub_code']].super.append(row['super_code'])
        for row in Db.get_translations(app.config['LANGUAGES']):
            properties[row['property_code']].i18n[row['language_code']] = \
                row['text']
            properties[row['property_code']].i18n_inverse[
                row['language_code']] = row['text_inverse']
        return properties
