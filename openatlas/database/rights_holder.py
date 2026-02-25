from typing import Any

from flask import g


def get_rights_holder() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id as id_,
               name,
               class as class_,
               description,
               created,
               modified
        FROM model.rights_holder
        """)
    return list(g.cursor)


def get_rights_holder_by_id(id_: int) -> dict[str, Any] | None:
    g.cursor.execute(
        """
        SELECT id as id_,
               name,
               class as class_,
               description,
               created,
               modified
        FROM model.rights_holder
        WHERE id = %(id)s
        """,
        {'id': id_})
    return g.cursor.fetchone()


def insert_rights_holder(entry: dict[str, Any]) -> int:
    g.cursor.execute(
        """
        INSERT INTO model.rights_holder (
            name,
            class,
            description)
        VALUES (
            %(name)s,
            %(role)s,
            %(description)s)
        RETURNING id;
        """,
        entry)
    return g.cursor.fetchone()['id']


def update_rights_holder(id_: int, entry: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE model.rights_holder
        SET name = %(name)s,
            class = %(role)s,
            description = %(description)s
        WHERE id = %(id)s
        """,
        {'id': id_, **entry})
