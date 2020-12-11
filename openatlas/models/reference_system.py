from typing import List, Optional

from flask import g
from flask_login import current_user
from flask_wtf import FlaskForm

from openatlas.models.entity import Entity
from openatlas.models.link import Link
from openatlas.models.node import Node
from openatlas.util.display import uc_first


class ReferenceSystem:
    # Tools for reference systems like Wikidata or GeoNames

    @staticmethod
    def get_all() -> List:
        entities = Entity.get_by_system_type('external reference')
        if not entities:
            return []
        return []
