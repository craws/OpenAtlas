from typing import Any, Dict, List

from flask import g


class CidocClass:

    @staticmethod
    def get_classes() -> List[Dict[str, Any]]:
        g.cursor.execute("""
            SELECT c.id, c.code, c.name, comment, COUNT(e.id) AS count
            FROM model.cidoc_class c
            LEFT JOIN model.entity e ON c.code = e.cidoc_class_code
            GROUP BY (c.id, c.name, c.comment);""")
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_hierarchy() -> List[Dict[str, Any]]:
        g.cursor.execute(
            "SELECT super_code, sub_code FROM model.cidoc_class_inheritance;")
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_translations(language_codes: List[str]) -> List[Dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT class_code, language_code, text FROM model.cidoc_class_i18n
            WHERE language_code IN %(language_codes)s;""",
            {'language_codes': tuple(language_codes)})
        return [dict(row) for row in g.cursor.fetchall()]
