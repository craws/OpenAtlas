from __future__ import annotations

from typing import Any, TYPE_CHECKING

from openatlas.database import overlay as db
from openatlas.display.util import get_file_path

if TYPE_CHECKING:  # pragma: no cover
    from openatlas.models.entity import Entity


class Overlay:
    def __init__(self, row: dict[str, Any]) -> None:
        self.id = row['id']
        self.name = row['name'] if 'name' in row else ''
        self.image_id = row['image_id']
        self.bounding_box = row['bounding_box']
        path = get_file_path(row['image_id'])
        self.image_name = path.name if path else False

    @staticmethod
    def insert(data: dict[str, Any]) -> None:
        db.insert({
            'image_id': data['image_id'],
            'bounding_box':
                f"[[{data['top_left_northing']}, "
                f"{data['top_left_easting']}], "
                f"[{data['top_right_northing']}, "
                f"{data['top_right_easting']}], "
                f"[{data['bottom_left_northing']}, "
                f"{data['bottom_left_easting']}]]"})

    @staticmethod
    def update(data: dict[str, Any]) -> None:
        db.update({
            'image_id': data['image_id'],
            'bounding_box':
                f"[[{data['top_left_northing']}, "
                f"{data['top_left_easting']}], "
                f"[{data['top_right_northing']}, "
                f"{data['top_right_easting']}], "
                f"[{data['bottom_left_northing']}, "
                f"{data['bottom_left_easting']}]]"})

    @staticmethod
    def get_by_object(object_: Entity) -> dict[int, Overlay]:
        places = [object_] + list(
            object_.get_linked_entities_recursive('P46', True))
        ids = []
        for place in places:
            for reference in place.get_linked_entities('P67', inverse=True):
                if reference.class_.name == 'file':
                    ids.append(reference.id)
        if not ids:
            return {}
        return {row['image_id']: Overlay(row) for row in db.get_by_object(ids)}

    @staticmethod
    def get_by_id(id_: int) -> Overlay:
        return Overlay(db.get_by_id(id_))

    @staticmethod
    def remove(id_: int) -> None:
        db.remove(id_)
