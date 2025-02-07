from typing import Any

from flask import g


def get_classes() -> list[dict[str, Any]]:
    g.cursor.execute("SELECT * FROM model.cidoc_classes;" )
    return list(g.cursor)


def get_hierarchy() -> list[dict[str, Any]]:
    g.cursor.execute(
        'SELECT super_code, sub_code FROM model.cidoc_class_inheritance;')
    return list(g.cursor)


def get_translations(language_codes: list[str]) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT class_code, language_code, text
        FROM model.cidoc_class_i18n
        WHERE language_code IN %(language_codes)s;
        """,
        {'language_codes': tuple(language_codes)})
    return list(g.cursor)
