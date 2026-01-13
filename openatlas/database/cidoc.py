from typing import Any

from flask import g


def cidoc_classes(with_count: bool = False) -> list[dict[str, Any]]:
    g.cursor.execute(
        f"""
        SELECT
            c.code,
            c.name,
            comment
            {', COUNT(e.id) AS count' if with_count else ''}
        FROM model.cidoc_class c
        {''' LEFT JOIN model.entity e ON c.code = e.cidoc_class_code
        GROUP BY (c.code, c.name, c.comment)''' if with_count else ''}
        ;
        """)
    return list(g.cursor)


def class_hierarchy() -> list[dict[str, Any]]:
    g.cursor.execute(
        'SELECT super_code, sub_code FROM model.cidoc_class_inheritance;')
    return list(g.cursor)


def class_translations(language_codes: list[str]) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT class_code, language_code, text
        FROM model.cidoc_class_i18n
        WHERE language_code IN %(language_codes)s;
        """,
        {'language_codes': tuple(language_codes)})
    return list(g.cursor)


def cidoc_properties(with_count: bool = False) -> list[dict[str, Any]]:
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
                p.name_inverse)''' if with_count else ''};
        """)
    return list(g.cursor)


def property_hierarchy() -> list[dict[str, Any]]:
    g.cursor.execute(
        'SELECT super_code, sub_code FROM model.property_inheritance;')
    return list(g.cursor)


def property_translations(language_codes: list[str]) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT property_code, language_code, text, text_inverse
        FROM model.property_i18n
        WHERE language_code IN %(language_codes)s;
        """,
        {'language_codes': tuple(language_codes)})
    return list(g.cursor)
