from typing import Any

from flask import g


class Network:

    @staticmethod
    def get_edges(
            classes: list[str],
            properties: list[str]) -> list[dict[str, int]]:
        g.cursor.execute(
            """
            SELECT l.id, l.domain_id, l.range_id
            FROM model.link l
            JOIN model.entity e ON l.domain_id = e.id
                AND e.openatlas_class_name IN %(classes)s
            JOIN model.entity e2 ON l.range_id = e2.id
                AND e2.openatlas_class_name IN %(classes)s
            WHERE property_code IN %(properties)s;
            """,
            {'classes': tuple(classes), 'properties': tuple(properties)})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_entities(classes: list[str]) -> list[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT e.id, e.name, e.openatlas_class_name
            FROM model.entity e
            WHERE openatlas_class_name IN %(classes)s
            """,
            {'classes': tuple(classes)})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_object_mapping() -> dict[int, int]:
        g.cursor.execute(
            """
            SELECT e.id, l.range_id
            FROM model.entity e
            JOIN model.link l ON e.id = l.domain_id AND l.property_code = 'P53'
            JOIN model.entity e2 ON l.range_id = e2.id
                AND e2.openatlas_class_name = 'place';
            """)
        return {row['range_id']: row['id'] for row in g.cursor.fetchall()}
