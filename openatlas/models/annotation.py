from typing import Optional, Any

from flask_login import current_user

from openatlas.database.annotation import AnnotationImage as Db


class AnnotationImage:
    @staticmethod
    def get_by_id(id_: int) -> Optional[dict[str, Any]]:
        return Db.get_by_id(id_)

    @staticmethod
    def get_by_file(image_id: int) -> list[dict[str, Any]]:
        return Db.get_by_file(image_id)

    @staticmethod
    def insert_annotation_image(
            image_id: int,
            coordinates: str,
            annotation: Optional[str] = None) -> None:
        Db.insert({
            'image_id': image_id,
            'user_id': current_user.id,
            'entity_id': None,
            'coordinates': coordinates,
            'annotation': annotation})

    @staticmethod
    def delete(id_: int) -> None:
        Db.delete(id_)
