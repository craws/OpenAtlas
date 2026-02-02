from __future__ import annotations

import json
import re
from typing import Any, Optional

from openatlas.database import annotation as db
from openatlas.display.util2 import sanitize


class AnnotationImage:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data['id']
        self.image_id = data['image_id']
        self.entity_id = data['entity_id']
        self.coordinates = data['coordinates']
        self.text = data['text']
        self.created = data['created']

    def update(
            self,
            entity_id: Optional[int] = None,
            text: Optional[str] = None) -> None:
        db.update_annotation_image({
            'id': self.id,
            'entity_id': entity_id,
            'text': sanitize(text)})

    def delete(self) -> None:
        db.delete_annotation_image(self.id)

    @staticmethod
    def get_by_id(id_: int) -> AnnotationImage:
        return AnnotationImage(db.get_annotation_image_by_id(id_))

    @staticmethod
    def get_by_file_id(id_: int) -> list[AnnotationImage]:
        return [
            AnnotationImage(row) for row
            in db.get_annotation_image_by_file_id(id_)]

    @staticmethod
    def get_orphaned_annotations() -> list[AnnotationImage]:
        return [
            AnnotationImage(row) for row in db.get_annotation_image_orphans()]

    @staticmethod
    def remove_entity_from_annotation(
            annotation_id: int,
            entity_id: int) -> None:
        db.remove_entity_from_annotation_image(annotation_id, entity_id)

    @staticmethod
    def insert(
            image_id: int,
            coordinates: str,
            entity_id: Optional[int] = None,
            text: Optional[str] = None) -> None:
        db.insert_annotation_image({
            'image_id': image_id,
            'entity_id': entity_id or None,
            'coordinates': coordinates,
            'text': sanitize(text)})


class AnnotationText:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = data['id']
        self.source_id = data['source_id']
        self.entity_id = data['entity_id']
        self.source_root = data.get('source_root')  # for orphan checks
        self.link_start = data['link_start']
        self.link_end = data['link_end']
        self.text = data['text']
        self.created = data['created']

    @staticmethod
    def extract_annotations(text: str) -> dict[str, Any]:
        current_offset = 0
        if not text:
            return {'text': None, 'data': []}

        def replace_mark(match: Any) -> str:
            nonlocal current_offset
            metadata = json.loads(match.group(1))
            inner_text: str = match.group(2)
            start, end = match.span()
            adjusted_start = start + current_offset
            adjusted_end = adjusted_start + len(inner_text)
            data.append({
                'entity_id': metadata.get('entityId'),
                'text': metadata.get('comment'),
                'link_start': adjusted_start,
                'link_end': adjusted_end})
            current_offset += len(inner_text) - (end - start)
            return inner_text

        data: list[dict[str, Any]] = []
        pattern = r'<mark meta="(.*?)">(.*?)</mark>'
        text = text.replace('</p><p>', '\n\n')
        for item in ['<p>', '</p>', '<br class="ProseMirror-trailingBreak">']:
            text = text.replace(item, '')
        text = re.sub(r'(<br>\s*)+$', '', text)
        text = text.replace('<br>', '\n').replace('&quot;', '"')
        return {'text': re.sub(pattern, replace_mark, text), 'data': data}

    @staticmethod
    def delete_annotations_text(source_id: int) -> None:
        db.delete_annotations_text(source_id)

    @staticmethod
    def remove_entity_from_annotation(
            annotation_id: int,
            entity_id: int) -> None:
        db.remove_entity_from_annotation_text(annotation_id, entity_id)

    @staticmethod
    def get_orphaned_annotations() -> list[AnnotationText]:
        return [
            AnnotationText(row) for row in db.get_annotation_text_orphans()]

    @staticmethod
    def get_by_source_id(id_: int) -> list[AnnotationText]:
        return [
            AnnotationText(row) for row
            in db.get_annotation_text_by_source_id(id_)]

    @staticmethod
    def insert(data: dict[str, Any]) -> None:
        db.insert_annotation_text(data)
