from __future__ import annotations

from typing import Any

from flask import g

from openatlas.database.rights_holder import (
    delete_rights_holder_links, get_entity_ids_by_rights_holder,
    get_rights_holder, get_rights_holder_by_id,
    get_rights_holder_links,
    get_rights_holders_by_entity_and_role, insert_rights_holder,
    insert_rights_holder_link, rights_holder_delete, update_rights_holder)
from openatlas.models.entity import Entity
from openatlas.models.openatlas_class import OpenatlasClass


class RightsHolder(Entity):

    def __init__(self, data: dict[str, Any]) -> None:
        is_actor = data.get('openatlas_class_name') == 'actor'
        if is_actor:
            data['openatlas_class_name'] = 'person'

        super().__init__(data)

        if is_actor:
            self.class_ = OpenatlasClass(
                name='actor',
                cidoc_class=g.cidoc_classes['E39'],
                hierarchies=[],
                reference_systems=[],
                new_types_allowed=False,
                standard_type_id=None,
                write_access='',
                attributes={},
                relations={},
                display={},
                extra={})
            self.cidoc_class = self.class_.cidoc_class
            self.openatlas_class_name = 'actor'


    @staticmethod
    def get_rights_holder() -> list[RightsHolder]:
        return [RightsHolder(item) for item in get_rights_holder()]

    @staticmethod
    def get_rights_holders_by_entity_and_role(
            entity_id: int,
            role: str) -> list[RightsHolder]:
        return [RightsHolder(item) for item in
                get_rights_holders_by_entity_and_role(entity_id, role)]

    @staticmethod
    def get_rights_holder_by_id(id_: int) -> RightsHolder | None:
        item = get_rights_holder_by_id(id_)
        return RightsHolder(item) if item else None

    @staticmethod
    def insert_rights_holder(entry: dict[str, Any]) -> int:
        return insert_rights_holder(entry)

    @staticmethod
    def update_rights_holder(id_: int, entry: dict[str, Any]) -> None:
        update_rights_holder(id_, entry)

    @staticmethod
    def rights_holder_delete(id_: int) -> None:
        rights_holder_delete(id_)

    @staticmethod
    def get_rights_holder_links() -> dict[int, dict[str, list[int]]]:
        return get_rights_holder_links()

    @staticmethod
    def get_rights_holder_information() -> dict[
            int, dict[str, list[RightsHolder]]]:
        rights_holder_dict = {rh.id: rh for rh in g.rights_holder}
        rights_holder_links = RightsHolder.get_rights_holder_links()
        result: dict[int, dict[str, list[RightsHolder]]] = {}
        for entity_id, links in rights_holder_links.items():
            result[entity_id] = {
                'creator': [
                    rights_holder_dict[rh_id]
                    for rh_id in links['creator']
                    if rh_id in rights_holder_dict],
                'license_holder': [
                    rights_holder_dict[rh_id]
                    for rh_id in links['license_holder']
                    if rh_id in rights_holder_dict]}
        return result

    @staticmethod
    def insert_rights_holder_link(
            entity_id: int,
            rights_holder_id: int,
            role: str) -> None:
        insert_rights_holder_link(entity_id, rights_holder_id, role)

    @staticmethod
    def delete_rights_holder_links(entity_id: int) -> None:
        delete_rights_holder_links(entity_id)

    @staticmethod
    def get_files_by_rights_holder_id(
            rights_holder_id: int) -> list[Entity]:
        return Entity.get_by_ids(
            get_entity_ids_by_rights_holder(rights_holder_id))
