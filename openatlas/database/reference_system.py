from typing import Any

from flask import g


class ReferenceSystem:

    @staticmethod
    def get_all() -> list[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT
                e.id, e.name,
                e.cidoc_class_code,
                e.description,
                e.openatlas_class_name,
                e.created,
                e.modified,
                rs.website_url,
                rs.resolver_url,
                rs.identifier_example,
                rs.system,
                COUNT(l.id) AS count,                
                array_to_json(
                    array_agg((t.range_id, t.description))
                        FILTER (WHERE t.range_id IS NOT NULL)
                ) AS types
            FROM model.entity e
            JOIN web.reference_system rs ON e.id = rs.entity_id
            LEFT JOIN model.link l ON e.id = l.domain_id
                AND l.property_code = 'P67'
            LEFT JOIN model.link t ON e.id = t.domain_id
                AND t.property_code = 'P2'
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
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def add_classes(entity_id: int, class_names: list[str]) -> None:
        for name in class_names:
            g.cursor.execute(
                """
                INSERT INTO web.reference_system_openatlas_class (
                    reference_system_id, openatlas_class_name)
                VALUES (%(entity_id)s, %(name)s);
                """,
                {'entity_id': entity_id, 'name': name})

    @staticmethod
    def remove_class(entity_id: int, class_name: str) -> None:
        g.cursor.execute(
            """
            DELETE FROM web.reference_system_openatlas_class
            WHERE reference_system_id = %(reference_system_id)s
                AND openatlas_class_name = %(class_name)s;
            """,
            {'reference_system_id': entity_id, 'class_name': class_name})

    @staticmethod
    def update_system(data: dict[str, Any]) -> None:
        g.cursor.execute(
            """
            UPDATE web.reference_system
            SET (
                name, 
                website_url, 
                resolver_url, 
                identifier_example
            ) = (
                %(name)s,
                %(website_url)s,
                %(resolver_url)s,
                %(identifier_example)s)
            WHERE entity_id = %(entity_id)s;
            """,
            data)

    @staticmethod
    def insert_system(data: dict[str, Any]) -> None:
        g.cursor.execute(
            """
            INSERT INTO web.reference_system (
                entity_id,
                name,
                website_url,
                resolver_url)
            VALUES (
                %(entity_id)s,
                %(name)s,
                %(website_url)s,
                %(resolver_url)s);
            """,
            data)

    @staticmethod
    def delete_links_from_entity(entity_id: int) -> None:
        g.cursor.execute(
            """
            DELETE FROM model.link l
            WHERE property_code = 'P67'
                AND domain_id IN %(systems_ids)s
                AND range_id = %(entity_id)s;
            """, {
                'systems_ids': tuple(g.reference_systems.keys()),
                'entity_id': entity_id})
