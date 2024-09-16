from typing import Any

from flask import g

ANNOTATION_IMAGE_SELECT = \
    """
    SELECT
        id,
        image_id,
        entity_id,
        coordinates,
        user_id,
        text,
        created
    FROM web.annotation_image
    """

ANNOTATION_TEXT_SELECT = \
    """
    SELECT
        id,
        source_id,
        entity_id,
        link_start,
        link_end,
        user_id,
        text,
        created
    FROM web.annotation_text
    """


def get_annotation_image_by_id(id_: int) -> dict[str, Any]:
    g.cursor.execute(
        ANNOTATION_IMAGE_SELECT + ' WHERE id =  %(id)s;',
        {'id': id_})
    return dict(g.cursor.fetchone()) if g.cursor.rowcount else {}


def get_annotation_text_by_id(id_: int) -> dict[str, Any]:
    g.cursor.execute(
        ANNOTATION_TEXT_SELECT + ' WHERE id =  %(id)s;',
        {'id': id_})
    return dict(g.cursor.fetchone()) if g.cursor.rowcount else {}


def get_annotation_image_by_file(image_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        ANNOTATION_IMAGE_SELECT + ' WHERE image_id =  %(image_id)s;',
        {'image_id': image_id})
    return [dict(row) for row in g.cursor.fetchall()]


def get_annotation_text_by_source(source_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        ANNOTATION_TEXT_SELECT + ' WHERE source_id =  %(source_id)s;',
        {'source_id': source_id})
    return [dict(row) for row in g.cursor.fetchall()]


def get_annotation_image_orphans() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            a.id,
            a.image_id,
            a.entity_id,
            a.coordinates,
            a.user_id,
            a.text,
            a.created
        FROM web.annotation_image a
        LEFT JOIN model.link l ON l.domain_id = a.image_id 
            AND l.range_id = a.entity_id 
            AND l.property_code = 'P67'
        WHERE l.id IS NULL AND a.entity_id IS NOT NULL
        """)
    return [dict(row) for row in g.cursor.fetchall()]


def insert_annotation_image(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.annotation_image (
            image_id,
            entity_id,
            coordinates,
            user_id,
            text
        ) VALUES (
            %(image_id)s,
            %(entity_id)s,
            %(coordinates)s,
            %(user_id)s,
            %(text)s);
        """,
        data)


def update_annotation_image(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE web.annotation_image
        SET (entity_id, text) = (%(entity_id)s, %(text)s)
        WHERE id = %(id)s;
        """,
        data)


def delete_annotation_image(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM web.annotation_image WHERE id = %(id)s;',
        {'id': id_})


def remove_entity_from_annotation_image(
        annotation_id: int,
        entity_id: int) -> None:
    g.cursor.execute(
        """
        UPDATE web.annotation_image
        SET entity_id = NULL
        WHERE id = %(annotation_id)s AND entity_id = %(entity_id)s;
        """,
        {'annotation_id': annotation_id, 'entity_id': entity_id})


def insert_annotation_text(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO web.annotation_text (
            source_id,
            entity_id,
            link_start,
            link_end,
            user_id,
            text
        ) VALUES (
            %(source_id)s,
            %(entity_id)s,
            %(link_start)s,
            %(link_end)s,
            %(user_id)s,
            %(text)s);
        """,
        data)
