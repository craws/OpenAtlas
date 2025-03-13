from typing import Any

from flask import g


def get_classes(with_count: bool = False) -> list[dict[str, Any]]:
    g.cursor.execute(
        f"""
        SELECT
            c.code,
            c.name,
            comment
            {', COUNT(e.id) AS count' if with_count else ''}
        FROM model.cidoc_class c
            {
            '''
            LEFT JOIN model.entity e ON c.code = e.cidoc_class_code
            GROUP BY (c.code, c.name, c.comment)''' if with_count else ''}
        ;
        """)
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
