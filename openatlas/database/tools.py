from typing import Any

from flask import g


def get_sex_types(entity_id: int) -> list[dict[str, Any]]:
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
        {'id': entity_id})
    return list(g.cursor)


def delete_sex_types(entity_id: int) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.link WHERE id IN (
            SELECT l.id
            FROM model.entity e
            JOIN model.link l ON l.range_id = e.id
                AND l.domain_id = %(id)s
                AND l.property_code = 'P2'
                AND e.openatlas_class_name = 'type_tools'
                AND e.name != 'Radiocarbon');
        """,
        {'id': entity_id})


def remove_bone_preservation_type(entity_id: int, type_ids: list[int]) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.link
        WHERE domain_id = %(entity_id)s AND range_id IN %(type_ids)s;
        """,
        {'entity_id': entity_id, 'type_ids': tuple(type_ids)})
