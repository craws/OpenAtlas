from typing import Any

from flask import g


def get_all() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            e.id,
            e.name,
            e.cidoc_class_code,
            e.description,
            e.openatlas_class_name,
            e.created,
            e.modified,
            rs.website_url,
            rs.resolver_url,
            rs.identifier_example,
            rs.reference_system_api_name AS api,
            rs.system,
            array_to_json(
                array_agg((t.range_id, t.description))
                    FILTER (WHERE t.range_id IS NOT NULL)
            ) AS types
        FROM model.entity e
        JOIN web.reference_system rs ON e.id = rs.entity_id
        LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code = 'P2'
        GROUP BY
            e.id,
            e.name,
            e.cidoc_class_code,
            e.description,
            e.openatlas_class_name,
            e.created,
            e.modified,
            rs.website_url,
            rs.resolver_url,
            rs.identifier_example,
            rs.system,
            rs.entity_id;
        """)
    return list(g.cursor)


def get_counts() -> dict[str, int]:
    g.cursor.execute(
        """
        SELECT e.id, COUNT(l.id) AS count
        FROM model.entity e
        LEFT JOIN model.link l ON e.id = l.domain_id
            AND l.property_code = 'P67'
        GROUP BY e.id;
        """)
    return {row['id']: row['count'] for row in list(g.cursor)}


def get_api_names() -> list[str]:
    g.cursor.execute(
        "SELECT name FROM web.reference_system_api ORDER BY name;")
    return [row[0] for row in list(g.cursor)]

def add_classes(entity_id: int, class_names: list[str]) -> None:
    for name in class_names:
        g.cursor.execute(
            """
            INSERT INTO web.reference_system_openatlas_class (
                reference_system_id, openatlas_class_name
            ) VALUES (%(entity_id)s, %(name)s);
            """,
            {'entity_id': entity_id, 'name': name})


def remove_class(entity_id: int, class_name: str) -> None:
    g.cursor.execute(
        """
        DELETE FROM web.reference_system_openatlas_class
        WHERE reference_system_id = %(reference_system_id)s
            AND openatlas_class_name = %(class_name)s;
        """,
        {'reference_system_id': entity_id, 'class_name': class_name})


def update_system(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE web.reference_system
        SET (
            name,
            website_url,
            resolver_url,
            identifier_example,
            reference_system_api_name
        ) = (
            %(name)s,
            %(website_url)s,
            %(resolver_url)s,
            %(identifier_example)s,
            %(api)s
        ) WHERE entity_id = %(entity_id)s;
        """,
        data)


def insert_system(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.reference_system (
            entity_id,
            name,
            website_url,
            resolver_url,
            reference_system_api_name)
        VALUES (
            %(entity_id)s,
            %(name)s,
            %(website_url)s,
            %(resolver_url)s,
            %(api)s);
        """,
        data)
