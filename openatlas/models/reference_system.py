from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, Optional, Union

from flask import g
from werkzeug.exceptions import abort

from openatlas.database.reference_system import ReferenceSystem as Db
from openatlas.models.entity import Entity


class ReferenceSystem(Entity):

    def __init__(self, row: dict[str, Any]) -> None:

        super().__init__(row)
        self.website_url = row['website_url']
        self.resolver_url = row['resolver_url']
        self.placeholder = row['identifier_example']
        self.precision_default_id = \
            list(self.types)[0].id if self.types else None
        self.count = row['count']
        self.system = row['system']
        self.classes: list[str] = []

    def update(self, data: dict[str, Any], new: bool = False,) -> Optional[int]:
        self.update_system(data)
        return super().update(data, new)

    @staticmethod
    def get_all() -> dict[int, ReferenceSystem]:
        systems = {row['id']: ReferenceSystem(row) for row in Db.get_all()}
        for class_ in g.classes.values():
            for system_id in class_.reference_systems:
                systems[system_id].classes.append(class_.name)
        return systems

    @staticmethod
    def get_by_name(name: str) -> ReferenceSystem:
        for system in g.reference_systems.values():
            if system.name == name:
                return system
        abort(404)  # pragma: no cover

    def remove_class(self, class_name: str) -> None:
        for link_ in self.get_links('P67'):
            if link_.range.class_.name == class_name:  # pragma: no cover
                return  # Abort if there are linked entities
        Db.remove_class(self.id, class_name)

    def update_system(self, data: dict[str, Any]) -> None:
        Db.update_system({
            'entity_id': self.id,
            'name': self.name,
            'website_url': data['reference_system']['website_url'],
            'resolver_url': data['reference_system']['resolver_url'],
            'identifier_example': data['reference_system']['placeholder']})
        if data['reference_system']['classes']:
            Db.add_classes(self.id, data['reference_system']['classes'])

    @staticmethod
    def delete_links_from_entity(entity: Entity) -> None:
        Db.delete_links_from_entity(entity.id)

    @staticmethod
    def get_class_choices(
            entity: Union[ReferenceSystem, None]) -> list[tuple[int, str]]:
        choices = []
        for class_ in g.classes.values():
            if not class_.reference_system_allowed \
                    or (entity and class_.name in entity.classes)\
                    or (
                        entity
                        and entity.name == 'GeoNames'
                        and class_.name != 'Place'):
                continue
            choices.append((class_.name, g.classes[class_.name].label))
        return choices

    @staticmethod
    def insert_system(data: dict[str, str]) -> Entity:
        entity = Entity.insert(
            'reference_system',
            data['name'],
            data['description'])
        Db.insert_system({
            'entity_id': entity.id,
            'name': entity.name,
            'website_url': data['website_url'] if data['website_url'] else None,
            'resolver_url': data['resolver_url']
            if data['resolver_url'] else None})
        return ReferenceSystem.get_all()[entity.id]
