from __future__ import annotations  # Needed for Python 4.0 type annotations

from typing import Any, Dict, List, Tuple, Union

from flask import g
from flask_wtf import FlaskForm

from openatlas.database.reference_system import ReferenceSystem as Db
from openatlas.models.entity import Entity


class ReferenceSystem(Entity):

    def __init__(self, row: Dict[str, Any]) -> None:

        super().__init__(row)
        self.website_url = row['website_url']
        self.resolver_url = row['resolver_url']
        self.placeholder = row['identifier_example']
        self.precision_default_id = \
            list(self.nodes.keys())[0].id if self.nodes else None
        self.count = row['count']
        self.system = row['system']
        self.classes: List[Dict[int, str]] = []

    @staticmethod
    def get_all() -> Dict[int, ReferenceSystem]:
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

    def add_classes(self, form: FlaskForm) -> None:
        Db.add_classes(self.id, form.classes.data)

    def remove_class(self, class_name: str) -> None:
        for link_ in self.get_links('P67'):
            if link_.range.class_.name == class_name:  # pragma: no cover
                return  # Abort if there are linked entities
        Db.remove_class(self.id, class_name)

    def update_system(self, form: FlaskForm) -> None:
        self.update(form)
        Db.update_system({
            'entity_id': self.id,
            'name': self.name,
            'website_url': self.website_url,
            'resolver_url': self.resolver_url,
            'identifier_example': self.placeholder})

    @staticmethod
    def update_links(form: FlaskForm, entity: Entity) -> None:
        for field in form:
            if field.id.startswith('reference_system_id_'):  # Recreate link
                system = Entity.get_by_id(
                    int(field.id.replace('reference_system_id_', '')))
                precision_field = getattr(
                    form,
                    field.id.replace('id_', 'precision_'))
                Db.remove_link(system.id, entity.id)
                if field.data:
                    system.link(
                        'P67',
                        entity,
                        field.data,
                        type_id=precision_field.data)

    @staticmethod
    def get_class_choices(
            entity: Union[ReferenceSystem, None]) -> List[Tuple[int, str]]:
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
    def insert_system(form: FlaskForm) -> Entity:
        entity = Entity.insert(
            'reference_system',
            form.name.data,
            form.description.data)
        Db.insert_system({
            'entity_id': entity.id,
            'name': entity.name,
            'website_url': form.website_url.data
            if form.website_url.data else None,
            'resolver_url': form.resolver_url.data
            if form.resolver_url.data else None})
        return ReferenceSystem.get_all()[entity.id]
