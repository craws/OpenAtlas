from typing import Any

from flask import g


def get_class_count() -> dict[str, int]:
    g.cursor.execute(
        """
        SELECT oc.name, COUNT(e.id) AS count
        FROM model.openatlas_class oc
        LEFT JOIN model.entity e ON oc.name = e.openatlas_class_name
        GROUP BY oc.name;
        """)
    return {row['name']: row['count'] for row in list(g.cursor)}


def get_classes() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            c.id,
            c.name,
            c.cidoc_class_code,
            c.standard_type_id,
            c.new_types_allowed,
            c.write_access_group_name,
            hierarchies,
            system_ids
        FROM model.openatlas_class c,
        LATERAL (
            SELECT json_agg(hierarchy_id) AS hierarchies FROM (
                SELECT hierarchy_id
                FROM web.hierarchy_openatlas_class hc
                JOIN web.hierarchy h ON hc.hierarchy_id = h.id
                WHERE c.name = hc.openatlas_class_name
                ORDER BY h.name) x) x,
        LATERAL (
            SELECT json_agg(reference_system_id) AS system_ids FROM (
                SELECT reference_system_id
                FROM web.reference_system_openatlas_class ro
                WHERE c.name = ro.openatlas_class_name) y) y
        ORDER BY c.name;
        """)
    return list(g.cursor)
