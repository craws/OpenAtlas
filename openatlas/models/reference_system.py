from __future__ import annotations

from typing import Any

from flask import g

from openatlas.database import reference_system as db
from openatlas.models.entity import Entity


class ReferenceSystem(Entity):
    def __init__(self, row: dict[str, Any]) -> None:
        super().__init__(row)
        self.website_url = row['website_url']
        self.resolver_url = row['resolver_url']
        self.placeholder = row['identifier_example']
        self.precision_default_id = \
            list(self.types)[0].id if self.types else None
        self.system = row['system']
        self.classes: list[str] = []

    def remove_class(self, name: str) -> None:
        db.remove_class(self.id, name)

    @staticmethod
    def get_all() -> dict[int, ReferenceSystem]:
        systems = {}
        for row in db.get_all():
            system = ReferenceSystem(row)
            for class_ in g.classes.values():
                if system.id in class_.reference_systems:
                    system.classes.append(class_.name)
            systems[system.id] = system
            if system.system:
                setattr(g, system.name.lower(), system)
        return systems

    @staticmethod
    def get_counts() -> dict[str, int]:
        return db.get_counts()

    @staticmethod
    def insert_system(data: dict[str, str]) -> ReferenceSystem:
        entity = Entity.insert(
            'reference_system',
            data['name'],
            data['description'])
        db.insert_system({
            'entity_id': entity.id,
            'name': entity.name,
            'website_url': data['website_url'] or None,
            'resolver_url': data['resolver_url'] or None})
        return ReferenceSystem.get_all()[entity.id]
