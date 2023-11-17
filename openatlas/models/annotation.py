from typing import Optional

from openatlas.database.annotation import AnnotationImage as Db


class AnnotationImage:

    @staticmethod
    def insert_annotation_image(
            file_id: int,
            coordinates: str,
            annotation: Optional[str] = None):
        # Db.insert(file_id, coordinates, annotation)
        pass

