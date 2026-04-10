from __future__ import annotations

from typing import Any

from flask import g

from openatlas.database import rights_holder as db


class RightsHolder:
    def __init__(self, data: dict[str, Any]) -> None:
        self.id = 0
        self.name = ''
        self.description = None
        self.class_ = None
        self.created = None
        self.modified = None
        self.aliases: dict[Any, Any] = {}
        for name, value in data.items():
            setattr(self, name, value)

    @staticmethod
    def get_rights_holder() -> list[RightsHolder]:
        return [RightsHolder(item) for item in db.get_rights_holder()]

    @staticmethod
    def get_rights_holders_by_entity_and_role(
            entity_id: int,
            role: str) -> list[RightsHolder]:
        return [RightsHolder(item) for item in
                db.get_rights_holders_by_entity_and_role(entity_id, role)]

    @staticmethod
    def get_rights_holder_by_id(id_: int) -> RightsHolder | None:
        item = db.get_rights_holder_by_id(id_)
        return RightsHolder(item) if item else None

    @staticmethod
    def insert_rights_holder(entry: dict[str, Any]) -> int:
        return db.insert_rights_holder(entry)

    @staticmethod
    def update_rights_holder(id_: int, entry: dict[str, Any]) -> None:
        db.update_rights_holder(id_, entry)

    @staticmethod
    def rights_holder_delete(id_: int) -> None:
        db.rights_holder_delete(id_)

    @staticmethod
    def get_rights_holder_links() -> dict[int, dict[str, list[int]]]:
        return db.get_rights_holder_links()

    @staticmethod
    def get_rights_holder_information() -> dict[
        int,
        dict[str, list[RightsHolder]]]:
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
        db.insert_rights_holder_link(entity_id, rights_holder_id, role)

    @staticmethod
    def delete_rights_holder_links(entity_id: int) -> None:
        db.delete_rights_holder_links(entity_id)

    @staticmethod
    def get_rights_holder_file_count() -> dict[int, int]:
        return db.get_rights_holder_file_count()
