from __future__ import annotations

from dataclasses import dataclass, field

from flask import g

from openatlas import app
from openatlas.database import cidoc_property as db


@dataclass
class CidocProperty:
    name: str
    name_inverse: str
    code: str
    comment: str
    domain_class_code: str
    range_class_code: str
    count: int = 0
    sub: list[int] = field(default_factory=lambda: [])
    super: list[int] = field(default_factory=lambda: [])
    i18n: dict[str, str] = field(default_factory=lambda: {})
    i18n_inverse: dict[str, str] = field(default_factory=lambda: {})

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


def get_cidoc_properties(
        language: str,
        with_count: bool = False) -> dict[str, CidocProperty]:
    properties = {
        row['code']:
            CidocProperty(**row) for row in db.get_properties(with_count)}
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
