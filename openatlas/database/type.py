from typing import Any

from flask import g


def get_types_without_count() -> list[dict[str, Any]]:
    g.cursor.execute("SELECT * FROM model.types_without_count;")
    return list(g.cursor)

def get_types_with_count() -> list[dict[str, Any]]:
    g.cursor.execute("SELECT * FROM model.types_with_count;")
    return list(g.cursor)



def get_hierarchies() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id, name, category, multiple, directional, required
        FROM web.hierarchy;
        """)
    return list(g.cursor)


def set_required(id_: int) -> None:
    g.cursor.execute(
        "UPDATE web.hierarchy SET required = true WHERE id = %(id)s;",
        {'id': id_})


def unset_required(id_: int) -> None:
    g.cursor.execute(
        "UPDATE web.hierarchy SET required = false WHERE id = %(id)s;",
        {'id': id_})


def set_selectable(id_: int) -> None:
    g.cursor.execute(
        "DELETE FROM web.type_none_selectable WHERE entity_id = %(id)s;",
        {'id': id_})


def unset_selectable(id_: int) -> None:
    g.cursor.execute(
        "INSERT INTO web.type_none_selectable (entity_id) VALUES (%(id)s)",
        {'id': id_})


def insert_hierarchy(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.hierarchy (id, name, multiple, category)
        VALUES (%(id)s, %(name)s, %(multiple)s, %(category)s);
        """,
        data)


def update_hierarchy(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE web.hierarchy
        SET name = %(name)s, multiple = %(multiple)s
        WHERE id = %(id)s;
        """,
        data)


def add_classes_to_hierarchy(type_id: int, class_names: list[str]) -> None:
    for class_name in class_names:
        g.cursor.execute(
            """
            INSERT INTO web.hierarchy_openatlas_class
                (hierarchy_id, openatlas_class_name)
            VALUES (%(type_id)s, %(class_name)s);
            """,
            {'type_id': type_id, 'class_name': class_name})


def move_link_type(data: dict[str, int]) -> None:
    g.cursor.execute(
        """
        UPDATE model.link
        SET type_id = %(new_type_id)s
        WHERE type_id = %(old_type_id)s AND id IN %(entity_ids)s;
        """,
        data)


def move_entity_type(data: dict[str, int]) -> None:
    g.cursor.execute(
        """
        UPDATE model.link
        SET range_id = %(new_type_id)s
        WHERE range_id = %(old_type_id)s AND domain_id IN %(entity_ids)s;
        """,
        data)


def remove_link_type(type_id: int, delete_ids: list[int]) -> None:
    g.cursor.execute(
        """
        UPDATE model.link
        SET type_id = NULL
        WHERE type_id = %(type_id)s AND id IN %(delete_ids)s;
        """,
        {'type_id': type_id, 'delete_ids': tuple(delete_ids)})


def remove_entity_type(type_id: int, delete_ids: list[int]) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.link
        WHERE range_id = %(type_id)s AND domain_id IN %(delete_ids)s;
        """,
        {'type_id': type_id, 'delete_ids': tuple(delete_ids)})


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


def remove_class(hierarchy_id: int, class_name: str) -> None:
    g.cursor.execute(
        """
        DELETE FROM web.hierarchy_openatlas_class
        WHERE hierarchy_id = %(hierarchy_id)s
            AND openatlas_class_name = %(class_name)s;
        """,
        {'hierarchy_id': hierarchy_id, 'class_name': class_name})


def remove_entity_links(type_id: int, entity_id: int) -> None:
    g.cursor.execute(
        """
        DELETE FROM model.link
        WHERE domain_id = %(entity_id)s
            AND range_id = %(type_id)s
            AND property_code = 'P2';
        """,
        {'entity_id': entity_id, 'type_id': type_id})
