from typing import Any

from flask import g


def get_properties(with_count: bool = False) -> list[dict[str, Any]]:

    g.cursor.execute(
        f"""
        SELECT
            p.code,
            p.comment,
            p.domain_class_code,
            p.range_class_code,
            p.name,
            p.name_inverse
            {', COUNT(l.id) AS count' if with_count else ''}
        FROM model.property p
            {'''
            LEFT JOIN model.link l ON p.code = l.property_code
            GROUP BY (
                p.code,
                p.comment,
                p.domain_class_code,
                p.range_class_code,
                p.name,
                p.name_inverse)''' if with_count else ''}
        ;
        """)
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
