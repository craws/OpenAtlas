from dataclasses import dataclass
from datetime import datetime
from typing import Any

from openatlas.database.rights_holder import (
    get_rights_holder, get_rights_holder_by_id, insert_rights_holder,
    update_rights_holder)


@dataclass
class RightsHolder:
    id_: int
    name: str
    class_: str
    description: str
    created: datetime
    modified: datetime

    @staticmethod
    def get_rights_holder() -> list["RightsHolder"]:
        return [RightsHolder(**item) for item in get_rights_holder()]

    @staticmethod
    def get(id_: int) -> "RightsHolder | None":
        item = get_rights_holder_by_id(id_)
        return RightsHolder(**item) if item else None

    @staticmethod
    def insert(entry: dict[str, Any]) -> int:
        return insert_rights_holder(entry)

    @staticmethod
    def update(id_: int, entry: dict[str, Any]) -> None:
        update_rights_holder(id_, entry)
