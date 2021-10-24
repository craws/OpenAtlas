from typing import Any, Dict, List, Union

from flask import g


class Node:

    @staticmethod
    def get_nodes(class_: str, property_: str) -> List[Dict[str, Any]]:
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
                es.id AS super_id,
                COUNT(l2.id) AS count,
                COUNT(l3.id) AS count_property,
                COALESCE(to_char(e.begin_from, 'yyyy-mm-dd BC'), '')
                    AS begin_from, e.begin_comment,
                COALESCE(to_char(e.begin_to, 'yyyy-mm-dd BC'), '') AS begin_to,
                COALESCE(to_char(e.end_from, 'yyyy-mm-dd BC'), '')
                    AS end_from, e.end_comment,
                COALESCE(to_char(e.end_to, 'yyyy-mm-dd BC'), '') AS end_to
            FROM model.entity e

            -- Get super
            LEFT JOIN model.link l ON e.id = l.domain_id
                AND l.property_code = %(property_code)s
            LEFT JOIN model.entity es ON l.range_id = es.id

            -- Get count
            LEFT JOIN model.link l2 ON e.id = l2.range_id
                AND l2.property_code IN ('P2', 'P89')
            LEFT JOIN model.link l3 ON e.id = l3.type_id

            WHERE e.openatlas_class_name = %(class)s
            GROUP BY e.id, es.id
            ORDER BY e.name;""",
            {'class': class_, 'property_code': property_})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def get_hierarchies() -> List[Dict[str, Any]]:
        g.cursor.execute("""
            SELECT h.id, h.name, h.category, h.multiple, h.directional,
                (SELECT ARRAY(
                    SELECT c.name
                    FROM model.openatlas_class c
                    JOIN web.hierarchy_openatlas_class hc 
                        ON c.id = hc.openatlas_class_id
                        AND hc.hierarchy_id = h.id)) AS class_names
            FROM web.hierarchy h;""")
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def insert_hierarchy(data: Dict[str, Any]) -> None:
        g.cursor.execute(
            """
            INSERT INTO web.hierarchy (id, name, multiple, category)
            VALUES (%(id)s, %(name)s, %(multiple)s, %(category)s);""", data)

    @staticmethod
    def update_hierarchy(data: Dict[str, Any]) -> None:
        g.cursor.execute(
            """
            UPDATE web.hierarchy
            SET name = %(name)s, multiple = %(multiple)s
            WHERE id = %(id)s;""", data)

    @staticmethod
    def add_form_to_hierarchy(node_id: int, form_ids: List[int]) -> None:
        for form_id in form_ids:
            g.cursor.execute(
                """
                INSERT INTO web.hierarchy_form (hierarchy_id, form_id)
                VALUES (%(node_id)s, %(form_id)s);""",
                {'node_id': node_id, 'form_id': form_id})

    @staticmethod
    def move_link_type(data: Dict[str, int]) -> None:
        g.cursor.execute(
            """
            UPDATE model.link SET type_id = %(new_type_id)s
            WHERE type_id = %(old_type_id)s AND id IN %(entity_ids)s;""", data)

    @staticmethod
    def move_entity_type(data: Dict[str, int]) -> None:
        sql = """
            UPDATE model.link SET range_id = %(new_type_id)s
            WHERE range_id = %(old_type_id)s AND domain_id IN %(entity_ids)s;"""
        g.cursor.execute(sql, data)

    @staticmethod
    def remove_link_type(type_id: int, delete_ids: List[int]) -> None:
        g.cursor.execute(
            """
            UPDATE model.link SET type_id = NULL
            WHERE type_id = %(type_id)s AND id IN %(delete_ids)s;""",
            {'type_id': type_id, 'delete_ids': tuple(delete_ids)})

    @staticmethod
    def remove_entity_type(type_id: int, delete_ids: List[int]) -> None:
        g.cursor.execute(
            """
            DELETE FROM model.link
            WHERE range_id = %(type_id)s AND domain_id IN %(delete_ids)s;""",
            {'type_id': type_id, 'delete_ids': tuple(delete_ids)})

    @staticmethod
    def get_form_count(form_id: int, node_ids: List[int]) -> int:
        # Todo: add types to forms
        return 0
        # g.cursor.execute(
        #     "SELECT name FROM web.form WHERE id = %(form_id)s;",
        #     {'form_id': form_id})
        # form_name = g.cursor.fetchone()['name']
        # g.cursor.execute(
        #     """
        #     SELECT COUNT(*) FROM model.link l
        #     JOIN model.entity e ON l.domain_id = e.id
        #         AND l.range_id IN %(node_ids)s
        #     WHERE l.property_code = 'P2'
        #         AND e.openatlas_class_name = %(form_name)s;""",
        #     {'node_ids': tuple(node_ids), 'form_name': form_name})
        # return g.cursor.fetchone()['count']

    @staticmethod
    def remove_form_from_hierarchy(form_id: int, hierarchy_id: int) -> None:
        g.cursor.execute(
            """
            DELETE FROM web.hierarchy_form
            WHERE hierarchy_id = %(hierarchy_id)s AND form_id = %(form_id)s;""",
            {'hierarchy_id': hierarchy_id, 'form_id': form_id})

    @staticmethod
    def remove_by_entity_and_node(entity_id: int, node_id: int) -> None:
        g.cursor.execute(
            """
            DELETE FROM model.link
            WHERE domain_id = %(entity_id)s
                AND range_id = %(node_id)s
                AND property_code = 'P2';""",
            {'entity_id': entity_id, 'node_id': node_id})
