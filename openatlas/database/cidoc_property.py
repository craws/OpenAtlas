from typing import Any

from flask import g


def get_properties() -> list[dict[str, Any]]:
    g.cursor.execute("SELECT * FROM model.cidoc_properties;")
    return list(g.cursor)


def get_hierarchy() -> list[dict[str, Any]]:
    g.cursor.execute(
        'SELECT super_code, sub_code FROM model.property_inheritance;')
    return list(g.cursor)


def get_translations(language_codes: list[str]) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT property_code, language_code, text, text_inverse
        FROM model.property_i18n
        WHERE language_code IN %(language_codes)s;
        """,
        {'language_codes': tuple(language_codes)})
    return list(g.cursor)
