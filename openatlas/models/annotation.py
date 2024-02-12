from __future__ import annotations

from typing import Any, Optional

from flask_login import current_user

from openatlas.database.annotation import AnnotationImage as Db


class Annotation:

    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data['id']
        self.image_id = data['image_id']
        self.entity_id = data['entity_id']
        self.coordinates = data['coordinates']
        self.user_id = data['user_id']
        self.text = data['annotation']
        self.created = data['created']

    def update(
            self,
            entity_id: Optional[int] = None,
            text: Optional[str] = None) -> None:
        Db.update({
            'id': self.id,
            'entity_id': entity_id,
            'annotation': text})

    def delete(self) -> None:
        Db.delete(self.id)

    @staticmethod
    def get_by_id(id_: int) -> Annotation:
        return Annotation(Db.get_by_id(id_))

    @staticmethod
    def get_by_file(image_id: int) -> list[Annotation]:
        return [Annotation(row) for row in Db.get_by_file(image_id)]

    @staticmethod
    def insert(
            image_id: int,
            coordinates: str,
            entity_id: Optional[int] = None,
            text: Optional[str] = None) -> None:
        Db.insert({
            'image_id': image_id,
            'user_id': current_user.id,
            'entity_id': entity_id or None,
            'coordinates': coordinates,
            'annotation': text})
