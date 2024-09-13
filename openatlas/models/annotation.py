from __future__ import annotations

from typing import Any, Optional

from flask_login import current_user

from openatlas.database import annotation as db


class Annotation:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data['id']
        self.image_id = data['image_id']
        self.entity_id = data['entity_id']
        self.coordinates = data['coordinates']
        self.user_id = data['user_id']
        self.text = data['text']
        self.created = data['created']

    def update(
            self,
            entity_id: Optional[int] = None,
            text: Optional[str] = None) -> None:
        db.update({'id': self.id, 'entity_id': entity_id, 'text': text})

    def delete(self) -> None:
        db.delete(self.id)

    @staticmethod
    def get_by_id(id_: int) -> Annotation:
        return Annotation(db.get_by_id(id_))

    @staticmethod
    def get_by_file(image_id: int) -> list[Annotation]:
        return [Annotation(row) for row in db.get_by_file(image_id)]

    @staticmethod
    def get_orphaned_annotations() -> list[Annotation]:
        return [Annotation(row) for row in db.get_orphaned_annotations()]

    @staticmethod
    def remove_entity_from_annotation(
            annotation_id: int,
            entity_id: int) -> None:
        db.remove_entity(annotation_id, entity_id)

    @staticmethod
    def insert(
            image_id: int,
            coordinates: str,
            entity_id: Optional[int] = None,
            text: Optional[str] = None) -> None:
        db.insert({
            'image_id': image_id,
            'user_id': current_user.id,
            'entity_id': entity_id or None,
            'coordinates': coordinates,
            'text': text})
