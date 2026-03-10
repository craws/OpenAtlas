from typing import Any

from flask import g

from openatlas.database.rights_holder import (
    delete_rights_holder_links, get_rights_holder, get_rights_holder_by_id,
    get_rights_holder_links,
    get_rights_holders_by_entity_and_role, insert_rights_holder,
    insert_rights_holder_link, update_rights_holder)
from openatlas.models.entity import Entity


class RightsHolder:

    @staticmethod
    def get_rights_holder() -> list[Entity]:
        return [Entity(item) for item in get_rights_holder()]

    @staticmethod
    def get_rights_holders_by_entity_and_role(
            entity_id: int,
            role: str) -> list[Entity]:
        return [Entity(item) for item in
                get_rights_holders_by_entity_and_role(entity_id, role)]

    @staticmethod
    def get_rights_holder_by_id(id_: int) -> Entity | None:
        item = get_rights_holder_by_id(id_)
        return Entity(item) if item else None

    @staticmethod
    def insert_rights_holder(entry: dict[str, Any]) -> int:
        return insert_rights_holder(entry)

    @staticmethod
    def update_rights_holder(id_: int, entry: dict[str, Any]) -> None:
        update_rights_holder(id_, entry)

    @staticmethod
    def get_rights_holder_links() -> dict[int, dict[str, list[int]]]:
        return get_rights_holder_links()

    @staticmethod
    def get_rights_holder_information() -> dict[int, dict[str, list[Entity]]]:
        rights_holder_dict = {rh.id: rh for rh in g.rights_holder}
        rights_holder_links = RightsHolder.get_rights_holder_links()
        result: dict[int, dict[str, list[Entity]]] = {}
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
