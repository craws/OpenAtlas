from typing import Any

from flask import g

SELECT = """
    SELECT
        id,
        image_id,
        entity_id,
        coordinates,
        user_id,
        annotation,
        created
    FROM web.annotation_image
    """


def get_by_id(id_: int) -> dict[str, Any]:
    g.cursor.execute(SELECT + ' WHERE id =  %(id)s;', {'id': id_})
    return dict(g.cursor.fetchone()) if g.cursor.rowcount else {}


def get_by_file(image_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        SELECT + ' WHERE image_id =  %(image_id)s;',
        {'image_id': image_id})
    return [dict(row) for row in g.cursor.fetchall()]


def get_orphaned_annotations() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            a.id,
            a.image_id,
            a.entity_id,
            a.coordinates,
            a.user_id,
            a.annotation,
            a.created
        FROM web.annotation_image a
        LEFT JOIN model.link l ON l.domain_id = a.image_id 
            AND l.range_id = a.entity_id 
            AND l.property_code = 'P67'
        WHERE l.id IS NULL AND a.entity_id IS NOT NULL
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def insert(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.annotation_image (
            image_id,
            entity_id,
            coordinates,
            user_id,
            annotation
        ) VALUES (
            %(image_id)s,
            %(entity_id)s,
            %(coordinates)s,
            %(user_id)s,
            %(annotation)s);
        """,
        data)


def update(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE web.annotation_image
        SET (entity_id, annotation) = (%(entity_id)s, %(annotation)s)
        WHERE id = %(id)s;
        """,
        data)


def delete(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM web.annotation_image WHERE id = %(id)s;',
        {'id': id_})


def remove_entity(annotation_id: int, entity_id: int) -> None:
    g.cursor.execute(
        """
        UPDATE web.annotation_image
        SET entity_id = NULL
        WHERE id = %(annotation_id)s AND entity_id = %(entity_id)s;
        """,
        {'annotation_id': annotation_id, 'entity_id': entity_id})
