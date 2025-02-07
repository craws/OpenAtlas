from typing import Any

from flask import g


def get_all() -> list[dict[str, Any]]:
    g.cursor.execute("SELECT * FROM model.reference_systems")
    return list(g.cursor)


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
            identifier_example
        ) = (
            %(name)s,
            %(website_url)s,
            %(resolver_url)s,
            %(identifier_example)s
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
            resolver_url)
        VALUES (
            %(entity_id)s,
            %(name)s,
            %(website_url)s,
            %(resolver_url)s);
        """,
        data)
