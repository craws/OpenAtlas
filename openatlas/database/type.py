from typing import Any

from flask import g


class Type:

    @staticmethod
    def get_types(with_count: bool) -> list[dict[str, Any]]:
        sql = f"""
            SELECT
                e.id,
                e.name,
                e.cidoc_class_code,
                e.description,
                e.openatlas_class_name,
                e.created,
                e.modified,
                es.id AS super_id,
                {'COUNT(l2.id)' if with_count else '0'} AS count,
                {'COUNT(l3.id)' if with_count else '0'} AS count_property,

                COALESCE(to_char(e.begin_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                    AS begin_from,
                COALESCE(to_char(e.begin_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                    AS begin_to,
                COALESCE(to_char(e.end_from, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                    AS end_from,
                COALESCE(to_char(e.end_to, 'yyyy-mm-dd hh24:mi:ss BC'), '')
                    AS end_to,
                e.begin_comment,
                e.end_comment
            FROM model.entity e

            -- Get super
            LEFT JOIN model.link l ON e.id = l.domain_id
                AND l.property_code IN ('P127', 'P89')
            LEFT JOIN model.entity es ON l.range_id = es.id
            """
        if with_count:
            sql += """
                -- Get count
                LEFT JOIN model.link l2 ON e.id = l2.range_id
                    AND l2.property_code IN ('P2', 'P89')
                LEFT JOIN model.link l3 ON e.id = l3.type_id
                """
        sql += """
            WHERE e.openatlas_class_name
                IN ('administrative_unit', 'type', 'type_tools')
            GROUP BY e.id, es.id
            ORDER BY e.name;
            """
        g.cursor.execute(sql)
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_hierarchies() -> list[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT id, name, category, multiple, directional, required
            FROM web.hierarchy;
            """)
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def set_required(id_: int) -> None:
        g.cursor.execute(
            "UPDATE web.hierarchy SET required = true WHERE id = %(id)s;",
            {'id': id_})

    @staticmethod
    def unset_required(id_: int) -> None:
        g.cursor.execute(
            "UPDATE web.hierarchy SET required = false WHERE id = %(id)s;",
            {'id': id_})

    @staticmethod
    def insert_hierarchy(data: dict[str, Any]) -> None:
        g.cursor.execute(
            """
            INSERT INTO web.hierarchy (id, name, multiple, category)
            VALUES (%(id)s, %(name)s, %(multiple)s, %(category)s);
            """,
            data)

    @staticmethod
    def update_hierarchy(data: dict[str, Any]) -> None:
        g.cursor.execute(
            """
            UPDATE web.hierarchy
            SET name = %(name)s, multiple = %(multiple)s
            WHERE id = %(id)s;
            """,
            data)

    @staticmethod
    def add_classes_to_hierarchy(type_id: int, class_names: list[str]) -> None:
        for class_name in class_names:
            g.cursor.execute(
                """
                INSERT INTO web.hierarchy_openatlas_class
                    (hierarchy_id, openatlas_class_name)
                VALUES (%(type_id)s, %(class_name)s);
                """,
                {'type_id': type_id, 'class_name': class_name})

    @staticmethod
    def move_link_type(data: dict[str, int]) -> None:
        g.cursor.execute(
            """
            UPDATE model.link
            SET type_id = %(new_type_id)s
            WHERE type_id = %(old_type_id)s AND id IN %(entity_ids)s;
            """,
            data)

    @staticmethod
    def move_entity_type(data: dict[str, int]) -> None:
        g.cursor.execute(
            """
            UPDATE model.link
            SET range_id = %(new_type_id)s
            WHERE range_id = %(old_type_id)s AND domain_id IN %(entity_ids)s;
            """,
            data)

    @staticmethod
    def remove_link_type(type_id: int, delete_ids: list[int]) -> None:
        g.cursor.execute(
            """
            UPDATE model.link
            SET type_id = NULL
            WHERE type_id = %(type_id)s AND id IN %(delete_ids)s;
            """,
            {'type_id': type_id, 'delete_ids': tuple(delete_ids)})

    @staticmethod
    def remove_entity_type(type_id: int, delete_ids: list[int]) -> None:
        g.cursor.execute(
            """
            DELETE FROM model.link
            WHERE range_id = %(type_id)s AND domain_id IN %(delete_ids)s;
            """,
            {'type_id': type_id, 'delete_ids': tuple(delete_ids)})

    @staticmethod
    def get_class_count(name: str, type_ids: list[int]) -> int:
        g.cursor.execute(
            """
            SELECT COUNT(*) FROM model.link l
            JOIN model.entity e ON l.domain_id = e.id
                AND l.range_id IN %(type_ids)s
            WHERE l.property_code = 'P2'
                AND e.openatlas_class_name = %(class_name)s;
            """,
            {'type_ids': tuple(type_ids), 'class_name': name})
        return g.cursor.fetchone()['count']

    @staticmethod
    def remove_class(hierarchy_id: int, class_name: str) -> None:
        g.cursor.execute(
            """
            DELETE FROM web.hierarchy_openatlas_class
            WHERE hierarchy_id = %(hierarchy_id)s
                AND openatlas_class_name = %(class_name)s;
            """,
            {'hierarchy_id': hierarchy_id, 'class_name': class_name})

    @staticmethod
    def remove_entity_links(type_id: int, entity_id: int) -> None:
        g.cursor.execute(
            """
            DELETE FROM model.link
            WHERE domain_id = %(entity_id)s
                AND range_id = %(type_id)s
                AND property_code = 'P2';
            """,
            {'entity_id': entity_id, 'type_id': type_id})
