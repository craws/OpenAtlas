from typing import Any, Dict, List

from flask import g


class Model:

    @staticmethod
    def get_openatlas_classes() -> List[Dict[str, Any]]:
        g.cursor.execute("""
            SELECT
                c.id,
                c.name,
                c.cidoc_class_code,
                c.standard_type_id,
                c.alias_allowed,
                c.reference_system_allowed,
                c.new_types_allowed,
                c.write_access_group_name,
                c.layout_color,
                c.layout_icon,
                hierarchies,
                system_ids
            FROM model.openatlas_class c,
            LATERAL (
                SELECT json_agg(hierarchy_id) AS hierarchies FROM (
                    SELECT hierarchy_id
                    FROM web.hierarchy_openatlas_class hc
                    WHERE c.name = hc.openatlas_class_name) x) x,
            LATERAL (
                SELECT json_agg(reference_system_id) AS system_ids FROM (
                    SELECT reference_system_id
                    FROM web.reference_system_openatlas_class ro
                    WHERE c.name = ro.openatlas_class_name) y) y""")
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_classes() -> List[Dict[str, Any]]:
        g.cursor.execute("""
            SELECT c.id, c.code, c.name, comment, COUNT(e.id) AS count
            FROM model.cidoc_class c
            LEFT JOIN model.entity e ON c.code = e.cidoc_class_code
            GROUP BY (c.id, c.name, c.comment);""")
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_class_hierarchy() -> List[Dict[str, Any]]:
        g.cursor.execute(
            "SELECT super_code, sub_code FROM model.cidoc_class_inheritance;")
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_class_translations(
            language_codes: List[str]) -> List[Dict[str, Any]]:
        sql = """
            SELECT class_code, language_code, text FROM model.cidoc_class_i18n
            WHERE language_code IN %(language_codes)s;"""
        g.cursor.execute(sql, {'language_codes': tuple(language_codes)})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_properties() -> List[Dict[str, Any]]:
        g.cursor.execute("""
            SELECT
                p.id,
                p.code,
                p.comment,
                p.domain_class_code,
                p.range_class_code,
                p.name,
                p.name_inverse,
                COUNT(l.id) AS count
            FROM model.property p
            LEFT JOIN model.link l ON p.code = l.property_code
            GROUP BY (
                p.id,
                p.code,
                p.comment,
                p.domain_class_code,
                p.range_class_code,
                p.name,
                p.name_inverse);""")
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_property_hierarchy() -> List[Dict[str, Any]]:
        g.cursor.execute(
            'SELECT super_code, sub_code FROM model.property_inheritance;')
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_property_translations(
            language_codes: List[str]) -> List[Dict[str, Any]]:
        sql = """
            SELECT property_code, language_code, text, text_inverse
            FROM model.property_i18n
            WHERE language_code IN %(language_codes)s;"""
        g.cursor.execute(sql, {'language_codes': tuple(language_codes)})
        return [dict(row) for row in g.cursor.fetchall()]
