from typing import Any, Optional

import requests
from flask import g

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.type import Type


def get_or_create_type(hierarchy: Entity, type_name: str) -> Entity:
    if type_ := get_type_by_name(type_name):
        if type_.root[0] == hierarchy.id:
            return type_
    type_entity = Entity.insert('type', type_name)
    type_entity.link('P127', hierarchy)
    return type_entity


def get_type_by_name(type_name: str) -> Optional[Type]:
    type_ = None
    for type_id in g.types:
        if g.types[type_id].name == type_name:
            type_ = g.types[type_id]
    return type_


def get_exact_match() -> Entity:
    return get_or_create_type(
        Type.get_hierarchy('External reference match'), 'exact match')


def get_reference_system(name: str) -> Entity:
    return [i for i in g.reference_systems.values() if i.name == name][0]


def vocabs_requests(
        id_: Optional[str] = '',
        endpoint: Optional[str] = '',
        parameter: Optional[dict[str, str]] = '') -> dict[str, Any]:
    req = requests.get(
        f"{g.settings['vocabs_base_url']}{g.settings['vocabs_endpoint']}{id_}/"
        f"{endpoint}",
        params=parameter,
        timeout=360,
        auth=(app.config['VOCABS_USER'], app.config['VOCABS_PW']))
    return req.json()
