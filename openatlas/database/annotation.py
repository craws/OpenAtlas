from typing import Optional, Any

from flask import g


class AnnotationImage:

    @staticmethod
    def get_by_file(file_id: int) -> list[dict[str, Any]]:
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
            WHERE
                image_id =  %(file_id)s  
            """,
            {'file_id': file_id})
        return [dict(row) for row in g.cursor.fetchall()]

    @staticmethod
    def insert(data: dict[str, Any]) -> None:
        print('sql')
        print(data)
        g.cursor.execute(
            """
            INSERT INTO web.annotation_image (
                image_id, 
                entity_id, 
                coordinates, 
                user_id, 
                annotation
            ) VALUES (
                %(file_id)s,
                %(entity_id)s,
                %(coordinates)s,
                %(user_id)s,
                %(annotation)s);
            """,
            data)
