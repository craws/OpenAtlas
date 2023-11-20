from typing import Optional, Any

from flask_login import current_user

from openatlas.database.annotation import AnnotationImage as Db


class AnnotationImage:

    @staticmethod
    def get_by_file(file_id: int) -> list[dict[str, Any]]:
        return Db.get_by_file(file_id)

    @staticmethod
    def insert_annotation_image(
            file_id: int,
            coordinates: str,
            annotation: Optional[str] = None) -> None:
        print('model')
        Db.insert({
            'file_id': file_id,
            'user_id': current_user.id,
            'entity_id': None,
            'coordinates': coordinates,
            'annotation': annotation})
        pass
