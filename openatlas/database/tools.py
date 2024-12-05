from typing import Any

from flask import g


def get_sex_types(id_: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT e.id, l.id AS link_id, l.description
        FROM model.entity e
        JOIN model.link l ON l.range_id = e.id
            AND l.domain_id = %(id)s
            AND l.property_code = 'P2'
            AND e.openatlas_class_name = 'type_tools'
            AND e.name != 'Radiocarbon';
        """,
        {'id': id_})
    return list(g.cursor)
