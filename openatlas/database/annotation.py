from typing import Optional, Any

from flask import g


class AnnotationImage:

    @staticmethod
    def get_by_id(id_: int) -> Optional[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT
                image_id,
                entity_id,
                coordinates,
                user_id,
                annotation,
                created
            FROM web.annotation_image
            WHERE id =  %(id)s;
            """,
            {'id': id_})
        return dict(g.cursor.fetchone()) if g.cursor.rowcount else None

    @staticmethod
    def get_by_file(image_id: int) -> list[dict[str, Any]]:
        g.cursor.execute(
            """
            SELECT
                id,
                image_id,
                entity_id,
                coordinates,
                user_id,
                annotation,
                created
            FROM web.annotation_image
            WHERE image_id =  %(image_id)s;
            """,
            {'image_id': image_id})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
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

    @staticmethod
    def delete(id_: int) -> None:
        g.cursor.execute(
            'DELETE FROM web.annotation_image WHERE id = %(id)s;',
            {'id': id_})
