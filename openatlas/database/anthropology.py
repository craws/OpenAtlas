from typing import Any

from flask import g


class Anthropology:

    @staticmethod
    def get_types(id_: int) -> list[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT e.id, l.id AS link_id, l.description
            FROM model.entity e
            JOIN model.link l ON l.range_id = e.id
                AND l.domain_id = %(id)s
                AND l.property_code = 'P2'
                AND e.openatlas_class_name = 'type_anthropology';
            """,
            {'id': id_})
        return [dict(row) for row in g.cursor.fetchall()]
