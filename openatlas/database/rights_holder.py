from typing import Any

from flask import g


def get_rights_holder() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT id,
               name,
               class,
               created,
               modified
        FROM model.rights_holder
        """)
    return list(g.cursor)


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
