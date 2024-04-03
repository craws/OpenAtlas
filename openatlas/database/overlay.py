from typing import Any

from flask import g


def insert(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.map_overlay (
            image_id,
            bounding_box)
        VALUES (
            %(image_id)s,
            %(bounding_box)s);
        """,
        data)


def update(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE web.map_overlay
        SET bounding_box = %(bounding_box)s
        WHERE image_id = %(image_id)s;
        """,
        data)


def get_by_object(ids: list[int]) -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT o.id, o.image_id, o.bounding_box, i.name
        FROM web.map_overlay o
        JOIN model.entity i ON o.image_id = i.id
        WHERE o.image_id IN %(image_ids)s;
        """,
        {'image_ids': tuple(ids)})
    return [dict(row) for row in g.cursor.fetchall()]


def get_by_id(id_: int) -> dict[str, Any]:
    g.cursor.execute(
        """
        SELECT id, image_id, bounding_box
        FROM web.map_overlay
        WHERE id = %(id)s;
        """,
        {'id': id_})
    return dict(g.cursor.fetchone())


def remove(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM web.map_overlay WHERE id = %(id)s;',
        {'id': id_})
