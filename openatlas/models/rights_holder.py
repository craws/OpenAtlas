from dataclasses import dataclass
from datetime import datetime
from typing import Any

from openatlas.database.rights_holder import (
    get_rights_holder, insert_rights_holder)


@dataclass
class RightsHolder:
    id: int
    name: str
    class_: str
    description: str
    created: datetime
    modified: datetime

    @staticmethod
    def get_rights_holder() -> list[dict[str, Any]]:
        return get_rights_holder()

    @staticmethod
    def insert(entry: dict[str, Any]) -> int:
        return insert_rights_holder(entry)
