from typing import Any

from flask import g

ANNOTATION_IMAGE_SELECT = \
    """
    SELECT
        id,
        image_id,
        entity_id,
        coordinates,
        text,
        created
    FROM model.annotation_image
    """

ANNOTATION_TEXT_SELECT = \
    """
    SELECT
        id,
        source_id,
        entity_id,
        link_start,
        link_end,
        text,
        created
    FROM model.annotation_text
    """


def get_annotation_image_by_id(id_: int) -> dict[str, Any]:
    g.cursor.execute(
        ANNOTATION_IMAGE_SELECT + ' WHERE id =  %(id)s;',
        {'id': id_})
    return g.cursor.fetchone()



def get_annotation_text_by_id(id_: int) -> dict[str, Any]:
    g.cursor.execute(
        ANNOTATION_TEXT_SELECT + ' WHERE id =  %(id)s;',
        {'id': id_})
    return g.cursor.fetchone()


def get_annotation_image_by_file(image_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        ANNOTATION_IMAGE_SELECT + ' WHERE image_id =  %(image_id)s;',
        {'image_id': image_id})
    return list(g.cursor)


def get_annotation_text_by_source(source_id: int) -> list[dict[str, Any]]:
    g.cursor.execute(
        ANNOTATION_TEXT_SELECT +
        """
        WHERE source_id = %(source_id)s
        ORDER BY link_start;
        """,
        {'source_id': source_id})
    return list(g.cursor)


def get_annotation_image_orphans() -> list[dict[str, Any]]:
    g.cursor.execute(
        """
        SELECT
            a.id,
            a.image_id,
            a.entity_id,
            a.coordinates,
            a.text,
            a.created
        FROM model.annotation_image a
        LEFT JOIN model.link l ON l.domain_id = a.image_id 
            AND l.range_id = a.entity_id 
            AND l.property_code = 'P67'
        WHERE l.id IS NULL AND a.entity_id IS NOT NULL
        """)
    return list(g.cursor)


def insert_annotation_image(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO model.annotation_image (
            image_id,
            entity_id,
            coordinates,
            text
        ) VALUES (
            %(image_id)s,
            %(entity_id)s,
            %(coordinates)s,
            %(text)s);
        """,
        data)


def update_annotation_image(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        UPDATE model.annotation_image
        SET (entity_id, text) = (%(entity_id)s, %(text)s)
        WHERE id = %(id)s;
        """,
        data)


def delete_annotation_image(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM model.annotation_image WHERE id = %(id)s;',
        {'id': id_})


def update_annotation_text(data: dict[str, Any]) -> None:
    print(data)
    g.cursor.execute(
        """
        UPDATE model.annotation_text
        SET (entity_id, text, link_start, link_end) =
        (%(entity_id)s, %(text)s, %(link_start)s, %(link_end)s)
        WHERE id = %(id)s;
        """,
        data)


def delete_annotation_text(id_: int) -> None:
    g.cursor.execute(
        'DELETE FROM model.annotation_text WHERE id = %(id)s;',
        {'id': id_})


def remove_entity_from_annotation_image(
        annotation_id: int,
        entity_id: int) -> None:
    g.cursor.execute(
        """
        UPDATE model.annotation_image
        SET entity_id = NULL
        WHERE id = %(annotation_id)s AND entity_id = %(entity_id)s;
        """,
        {'annotation_id': annotation_id, 'entity_id': entity_id})


def insert_annotation_text(data: dict[str, Any]) -> None:
    g.cursor.execute(
        """
        INSERT INTO model.annotation_text (
            source_id,
            entity_id,
            link_start,
            link_end,
            text
        ) VALUES (
            %(source_id)s,
            %(entity_id)s,
            %(link_start)s,
            %(link_end)s,
            %(text)s);
        """,
        data)
