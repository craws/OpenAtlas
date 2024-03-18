from typing import Any, Optional

import requests
from flask import g

from openatlas import app
from openatlas.models.entity import Entity
from openatlas.models.type import Type


def get_or_create_type(hierarchy: Any, type_name: str) -> Entity:
    if type_ := get_type_by_name(type_name):
        if type_.root[0] == hierarchy.id:
            return type_
    type_entity = Entity.insert('type', type_name)  # pragma: no cover
    type_entity.link('P127', hierarchy)  # pragma: no cover
    return type_entity  # pragma: no cover


def get_type_by_name(type_name: str) -> Optional[Type]:
    type_ = None
    for type_id in g.types:
        if g.types[type_id].name == type_name:
            type_ = g.types[type_id]
    return type_


def get_exact_match() -> Entity:
    return get_or_create_type(g.reference_match_type, 'exact match')


def get_match_types() -> dict[str, Type]:
    match_dictionary = {}
    for match in [g.types[match] for match in g.reference_match_type.subs]:
        match match.name:
            case 'exact match':
                match_dictionary['exact_match'] = match
            case 'close match':
                match_dictionary['close_match'] = match
    return match_dictionary


def get_reference_system(name: str) -> Entity:  # pragma: no cover
    return [i for i in g.reference_systems.values() if i.name == name][0]


def vocabs_requests(
        id_: Optional[str] = '',
        endpoint: Optional[str] = '',
        parameter: Optional[dict[str, str]] = None) -> dict[str, Any]:
    req = requests.get(
        f"{g.settings['vocabs_base_url']}{g.settings['vocabs_endpoint']}{id_}/"
        f"{endpoint}",
        params=parameter or '',
        timeout=60,
        auth=(g.settings['vocabs_user'], app.config['VOCABS_PASS']))
    return req.json()


def request_arche_metadata(id_: int) -> dict[str, Any]:
    req = requests.get(
        f"{app.config['ARCHE']['url']}/api/{id_}/metadata",
        headers={
            'Accept': 'application/ld+json',
            'X-METADATA-READ-MODE': '1_1_0_0'},
        timeout=60)
    return req.json()
